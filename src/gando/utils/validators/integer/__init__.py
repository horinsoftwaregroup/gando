import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate(value):
    pattern = r'^([0]){1}$|^([1-9]){1}([0-9])*$'
    validation_error_message = _('Please enter a valid number.')

    value = str(value)
    if not re.match(pattern, value):
        raise ValidationError(validation_error_message)

    value = int(value)
    return value
