from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import signals
from django.template import Context, Template
from django.urls.base import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.module_loading import import_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from twilio.base.exceptions import TwilioException

from .. import constants
from ..fields import PhoneField
from .mixins import AuditableMixin


class MessageManager(models.Manager):
    def create_or_update_from_api(self, **kwargs):
        data = kwargs.get('data')
        assert data, "Data was not provided"

        from_number = data.get('From')
        to_number = data.get('To')
        content = data.get('Body')

        PhoneModel = import_string('core.models.Phone')
        phone = PhoneModel.objects.get(phone=to_number)
        company = phone.company
        customer = None

        if phone.company:
            customer = company.customer_set.filter(
                phone=from_number
            ).first()

        instance, created = self.update_or_create(
            api_id=data.get('MessageSid'),
            defaults=dict(
                company=company,
                content=content,
                customer=customer,
                date_send=timezone.now(),
                direction=constants.DIRECTION_INBOUND,
                from_number=from_number,
                to_number=to_number,
                type=constants.MESSAGE_SMS,
            )
        )
        return instance, created

    def create_sms(
        self, template_string, context={}, **kwargs
    ):
        assert 'direction' not in kwargs
        assert 'type' not in kwargs
        assert 'from_email' not in kwargs
        assert 'to_email' not in kwargs
        assert 'subject' not in kwargs

        instance = self.model(
            content=template_string,
            direction=constants.DIRECTION_OUTBOUND,
            type=constants.MESSAGE_SMS,
            **kwargs
        )
        instance.clean()
        instance.save()

        if 'message' not in context:
            context['message'] = instance
        if 'url' not in context:
            context['url'] = instance.get_public_url(**context)

        instance.content = Template(template_string).render(Context(context))
        instance.save(update_fields=['content'])
        return instance


class Message(AuditableMixin):
    company = models.ForeignKey(
        'core.Company', on_delete=models.CASCADE,
        verbose_name=_("Company")
    )
    customer = models.ForeignKey(
        'core.Customer', blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name=_("Customer")
    )
    type = models.SlugField(
        choices=constants.MESSAGE_CHOICES,
        editable=False,
        default=constants.MESSAGE_SMS,
        verbose_name=_("Type")
    )
    direction = models.SlugField(
        choices=constants.DIRECTION_CHOICES,
        editable=False,
        default=constants.DIRECTION_OUTBOUND,
        verbose_name=_("Direction")
    )
    date_send = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Send date")
    )
    date_read = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Read date")
    )
    from_number = PhoneField(
        blank=True,
        null=True,
        verbose_name=_("From number")
    )
    to_number = PhoneField(
        blank=True,
        null=True,
        verbose_name=_("To number")
    )
    from_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_("From email")
    )
    to_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_("To email")
    )
    api_id = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        verbose_name=_("API ID")
    )
    subject = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        verbose_name=_("Subject")
    )
    content = models.TextField(
        verbose_name=_("Content")
    )

    objects = MessageManager()

    class Meta:
        ordering = ['-date_creation']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def clean(self):
        super().clean()

        if self.type == constants.MESSAGE_SMS:
            if not self.from_number:
                raise ValidationError({
                    'from_number': _("This field is required.")
                })
            if not self.to_number:
                raise ValidationError({
                    'to_number': _("This field is required.")
                })
        elif self.type == constants.MESSAGE_EMAIL:
            if not self.from_email:
                raise ValidationError({
                    'from_email': _("This field is required.")
                })
            if not self.to_email:
                raise ValidationError({
                    'to_email': _("This field is required.")
                })

    def check_stop(self):
        if not self.customer:
            return False
        elif self.direction == constants.DIRECTION_OUTBOUND:
            return False
        elif self.type == constants.MESSAGE_EMAIL:
            return False

        stop_words = ('stop', 'end', 'cancel', 'unsubscribe', 'quit')
        content = self.content.lower().strip()
        if content not in stop_words:
            return False

        self.customer.send_sms = False
        self.customer.save(update_fields=['send_sms'])
        self.confirm_stop()
        return True

    def confirm_stop(self):
        cls = self.__class__

        content = (
            "You have been unsubscribed and will no longer receive any text."
        )

        instance = cls.objects.create_sms(
            company=self.company,
            template_string=content,
            from_number=self.to_number,
            to_number=self.from_number
        )
        instance.send()

    @property
    def from_(self):
        if self.type == constants.MESSAGE_SMS:
            return self.from_number
        elif self.type == constants.MESSAGE_EMAIL:
            return self.from_email

    def get_public_url(self, scheme=None, host=None, **kwargs):
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        url = reverse('public:message_redirect', args=[uid])
        if scheme and host:
            url = f'{scheme}://{host}{url}'
        return url

    @property
    def to(self):
        if self.type == constants.MESSAGE_SMS:
            return self.to_number
        elif self.type == constants.MESSAGE_EMAIL:
            return self.to_email

    def send(self):
        return getattr(self, f'send_{self.type}')()

    def send_sms(self):
        try:
            sender = self.company.sender
        except AttributeError:
            sender = None

        if not sender:
            raise ValidationError(
                _("Company must have a sender phone.")
            )

        if self.from_number != sender.phone:
            self.from_number = sender.phone

        client = sender.get_client()
        try:
            message = client.messages.create(
                body=self.content,
                from_=self.from_number,
                to=self.to_number
            )
            self.date_send = timezone.now()
            self.api_id = message.sid
            self.save(update_fields=['api_id', 'date_send'])
        except TwilioException as err:
            return err.msg if hasattr(err, 'msg') else err


def post_save(sender, instance, created, **kwargs):
    instance.check_stop()


signals.post_save.connect(post_save, sender=Message)
