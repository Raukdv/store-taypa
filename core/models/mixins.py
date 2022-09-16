from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField


class AuditableMixin(models.Model):
    date_creation = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date")
    )
    date_modification = models.DateTimeField(
        auto_now=True, verbose_name=_("Modification date")
    )

    class Meta:
        abstract = True


def get_address_mixin(required=False, default_country=None):
    class Mixin(models.Model):
        address = models.TextField(
            blank=not required,
            null=not required,
            verbose_name=_("Address")
        )
        address_2 = models.TextField(
            blank=True,
            null=True,
            verbose_name=_("Address 2")
        )
        city = models.CharField(
            blank=not required,
            max_length=150,
            null=not required,
            verbose_name=_("City")
        )
        state = models.CharField(
            blank=not required,
            max_length=150,
            null=not required,
            verbose_name=_("State")
        )
        country = CountryField(
            blank=not required,
            default=default_country,
            null=not required
        )

        class Meta:
            abstract = True

    return Mixin
