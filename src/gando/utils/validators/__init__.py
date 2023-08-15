from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^(\+[0-9]{2,})$"
    message = _(
        "Enter a valid phone_number(example: +989123456789)."
    )
    flags = 0
