from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .mixins import AuditableMixin
from ..fields import PhoneField


class Customer(AuditableMixin):
    company = models.ForeignKey(
        'core.Company', on_delete=models.CASCADE, verbose_name=_("Company")
    )
    first_name = models.CharField(
        _('first name'), max_length=150
    )
    last_name = models.CharField(
        _('last name'), max_length=150
    )
    email = models.EmailField(
        blank=True, null=True, verbose_name=_("email")
    )
    phone = PhoneField(
        blank=True, null=True, verbose_name=_("phone")
    )
    send_sms = models.BooleanField(
        default=True, verbose_name=_("Send SMS")
    )

    class Meta:
        ordering = ['-date_creation']
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.get_full_name()

    def clean(self):
        super().clean()
        if not any([self.email, self.phone]):
            raise ValidationError(_("Either an email or a phone is required."))

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def send(self, scheme, host):
        if self.email:
            self._send_email(scheme=scheme, host=host)
        if self.phone:
            self._send_sms(scheme=scheme, host=host)

    def _send_email(self, scheme, host):
        if not self.email:
            return

        message = self.message_set.create_html_template_email(
            template_name='panel/customer/review_email.html',
            to_email=self.email,
        )
        message.send(scheme=scheme, host=host)

    def _send_sms(self, scheme, host):
        if not self.phone:
            raise ValidationError(
                _("Customer must have a phone. Set it up first.")
            )

        try:
            sender = self.company.sender
        except AttributeError:
            sender = None

        if not sender:
            raise ValidationError(
                _("Company must have a sender phone, contact support.")
            )

        message = self.message_set.create_sms(
            customer=self,
            company=self.company,
            template_string=self.company.sms_template,
            from_number=sender.phone,
            to_number=self.phone,
            context=dict(
                company=self.company,
                customer=self,
                host=host,
                object=self,
                scheme=scheme,
            )
        )
        message.send()
