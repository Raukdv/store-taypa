from django.conf import settings
from django.db import models
from django.db.models import signals
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from twilio.rest import Client as TwilioClient, TwilioException

from .mixins import AuditableMixin
from ..fields import PhoneField


class PhoneManager(models.Manager):
    def purchase(self, request, phone):
        client = self.model.get_client()
        sms_url = reverse('public:message_sms')
        sms_url = f'{request.scheme}://{request.get_host()}{sms_url}'

        try:
            phone = client.incoming_phone_numbers.create(
                friendly_name=phone,
                phone_number=phone,
                sms_url=sms_url
            )
        except TwilioException as err:
            return err.msg if hasattr(err, 'msg') else err

        instance, created = self.update_or_create(
            api_id=phone.sid,
            defaults=dict(
                phone=phone.phone_number
            )
        )
        return instance

    def search(self, **kwargs):
        client = self.model.get_client()
        country = kwargs.pop('country')
        type_ = kwargs.pop('type')

        phone_list = client.available_phone_numbers(country)
        phone_list = getattr(phone_list, type_)
        return phone_list.list(**kwargs)

    def sync(self, request):
        client = self.model.get_client()

        try:
            phone_list = client.incoming_phone_numbers.list()
        except TwilioException as err:
            return err.msg if hasattr(err, 'msg') else err

        sms_url = reverse('public:message_sms')
        sms_url = f'{request.scheme}://{request.get_host()}{sms_url}'
        api_list = []

        for phone in phone_list:
            date_connection = (
                timezone.now() if phone.sms_url == sms_url else None
            )

            item, created = self.update_or_create(
                api_id=phone.sid,
                defaults=dict(
                    date_connection=date_connection,
                    phone=phone.phone_number
                )
            )
            api_list.append(item)

        for phone in self.all():
            if phone not in api_list:
                phone.delete()

        return api_list


class Phone(AuditableMixin):
    phone = PhoneField(
        unique=True, verbose_name=_("Phone")
    )
    api_id = models.CharField(
        max_length=100, verbose_name=_("API ID")
    )
    date_connection = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Connection date")
    )
    company = models.OneToOneField(
        'core.Company', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='sender', verbose_name=_("Company")
    )

    objects = PhoneManager()

    class Meta:
        ordering = ['phone']
        verbose_name = _("Phone")
        verbose_name_plural = _("Phones")

    def __str__(self):
        return str(self.phone)

    def connect(self, request):
        client = self.get_client()
        sms_url = reverse('public:message_sms')
        sms_url = f'{request.scheme}://{request.get_host()}{sms_url}'

        try:
            client \
                .incoming_phone_numbers(self.api_id) \
                .update(sms_url=sms_url)
        except TwilioException as err:
            return err.msg if hasattr(err, 'msg') else err

        self.date_connection = timezone.now()
        self.save(update_fields=['date_connection'])

    def api_delete(self):
        try:
            client = self.get_client()
            client.incoming_phone_numbers(sid=self.api_id).delete()
        except TwilioException:
            pass

    @classmethod
    def get_client(cls):
        return TwilioClient(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

    def is_connected(self):
        return True if self.date_connection else False
    is_connected.boolean = True


def pre_delete(sender, instance, **kwargs):
    instance.api_delete()


signals.pre_delete.connect(pre_delete, sender=Phone)
