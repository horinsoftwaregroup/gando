import uuid
from django.db import models


class AbstractBaseModel(models.Model):
    uid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    created_dt = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    updated_dt = models.DateTimeField(
        auto_now=True,
        db_index=True,
    )
    available = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        abstract = True
