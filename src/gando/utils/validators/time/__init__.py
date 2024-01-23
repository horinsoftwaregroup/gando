import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.timezone import now as dj_now

from datetime import datetime, time


def validate(value):
    pattern = r'^([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$'
    validation_error_message = _('Entered in the following format.\nhh:mm:ss')

    value = str(value)
    if not re.match(pattern, value):
        raise ValidationError(validation_error_message)

    n = dj_now()
    n = f'{n.year}-{n.month}-{n.day}'
    value = datetime.strptime(f'{n} {value}', '%Y-%m-%d %H:%M:%S')
    value = time(hour=value.hour, minute=value.minute, second=value.second)
    return value
