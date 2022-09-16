from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _

from . import validators


class PhoneField(CharField):
    default_validators = [validators.validate_phone]
    description = _("Comma-separated integers")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 30
        super().__init__(*args, **kwargs)
