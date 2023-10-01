from pydantic import BaseModel
from datetime import datetime


class AbstractBaseSchemaModel(BaseModel):
    id: int | None = None
    uid: str | None = None
    created_dt: datetime | None = None
    updated_dt: datetime | None = None
    available: int | None = None
