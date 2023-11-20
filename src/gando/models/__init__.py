from simple_history.models import HistoricalRecords
import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models


class AbstractBaseModel(models.Model):
    id = models.UUIDField(
        verbose_name=_('ID'),
        primary_key=True,
        default=uuid.uuid4,
        blank=False,
        null=False,
        unique=True,
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
        default=1,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
        db_index=True,
    )

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class AbstractBaseModelFaster(models.Model):
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
        default=1,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
        db_index=True,
    )

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
