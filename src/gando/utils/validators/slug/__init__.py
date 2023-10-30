from typing import Optional
import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate(value, pattern: Optional[str] = None, validation_error_message: Optional[str] = None):
    pattern = pattern or r'^[a-z0-9-]+$'
    validation_error_message = validation_error_message or _(
        'The value of this section should only contain lowercase letters, English numbers and - sign.')
    if not re.match(pattern, value):
        raise ValidationError(validation_error_message)
