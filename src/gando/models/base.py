from simple_history.models import HistoricalRecords
import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models


class AbstractBaseModel(models.Model):
    uid = models.UUIDField(
        verbose_name=_('UID'),
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    created_dt = models.DateTimeField(
        verbose_name=_('Created Datetime'),
        auto_now_add=True,
        db_index=True,
    )
    updated_dt = models.DateTimeField(
        verbose_name=_('Updated Datetime'),
        auto_now=True,
        db_index=True,
    )
    available = models.IntegerField(
        verbose_name=_('Available'),
        max_length=1,
        default=1,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
        db_index=True,
    )

    history = HistoricalRecords()

    class Meta:
        abstract = True
