from simple_history.models import HistoricalRecords
import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Manager as DjBaseManager, QuerySet


class BaseManager(DjBaseManager):
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(available=1)
        return queryset


class Manager(BaseManager.from_queryset(QuerySet)):
    pass


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

    objects = Manager()

    class Meta:
        abstract = True


class WhiteAbstractBaseModel(models.Model):
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
