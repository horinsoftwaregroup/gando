import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from datetime import datetime, date


def validate(value):
    pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,31}$'
    validation_error_message = _(
        "Please enter your password as a combination of "
        "uppercase English letters and "
        "lowercase English letters, "
        "English numbers and characters (!#*_-.).\n"
        "The minimum number of characters is 8 and the maximum is 31.")

    value = str(value)
    if not re.match(pattern, value):
        raise ValidationError(validation_error_message)
    return value
