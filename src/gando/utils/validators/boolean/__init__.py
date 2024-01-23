from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate(value):
    validation_error_message = _('Please enter a valid number.')

    value = str(value).lower()
    match value:
        case 't':
            return True
        case 'true':
            return True
        case '1':
            return True
        case 'f':
            return False
        case 'false':
            return False
        case '0':
            return False
        case _:
            raise ValidationError(validation_error_message)
