import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate(value):
    pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
    validation_error_message = _(
        "Please enter your email correctly. The correct email format is as follows."
        "example@example@example")

    value = str(value)
    if not re.match(pattern, value):
        raise ValidationError(validation_error_message)
    return value
