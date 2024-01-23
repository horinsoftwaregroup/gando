from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate(value):
    validation_error_message = _('Please enter a valid number.')

    value = str(value).lower()
    match value:
        case 't':
            value = True
        case 'true':
            value = True
        case '1':
            value = True
        case 'f':
            value = False
        case 'false':
            value = False
        case '0':
            value = False
        case _:

            raise ValidationError(validation_error_message)
