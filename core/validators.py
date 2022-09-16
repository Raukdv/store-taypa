from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _
import phonenumbers


def validate_phone(value):
    if value in EMPTY_VALUES:
        raise ValidationError(_("Invalid value."))

    if not isinstance(value, str):
        value = str(value)

    try:
        pn = phonenumbers.parse(value)
    except phonenumbers.phonenumberutil.NumberParseException as err:
        raise ValidationError(err._msg)

    if not all([
        phonenumbers.is_valid_number(pn),
        phonenumbers.is_possible_number(pn)
    ]):
        raise ValidationError(
            _("Not a possible or valir number.")
        )

    return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
