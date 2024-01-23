import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate(value):
    pattern = r"^[a-z]{1}[0-9a-z\-_]{3,31}$"
    validation_error_message = _(
        r"Please follow the format of your username correctly. "
        r"The minimum number of characters is 3 and the maximum number is 31."
        r"Please do not start your username with numbers and "
        r"symbols and do not use capital letters. "
        r"Try to use a combination of numbers and "
        r"signs (-,_) and English lowercase letters."
    )

    value = str(value)
    if not re.match(pattern, value):
        raise ValidationError(validation_error_message)
    return value
