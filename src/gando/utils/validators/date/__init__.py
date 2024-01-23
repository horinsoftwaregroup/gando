import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from datetime import datetime, date


def validate(value):
    pattern = r'^(18[0-9]{2}|19[0-9]{2}|2[0-9]{3})-(0[1-9]|1[012])-([123]0|[012][1-9]|31)$'
    validation_error_message = _(
        "The entered value must be greater than '1800-01-01' and "
        "entered in the following format.\nYYYY-MM-DD")

    value = str(value)
    if not re.match(pattern, value):
        raise ValidationError(validation_error_message)

    value = datetime.strptime(f'{value} 00:00:00', '%Y-%m-%d %H:%M:%S')
    value = date(year=value.year, month=value.month, day=value.day)
    return value
