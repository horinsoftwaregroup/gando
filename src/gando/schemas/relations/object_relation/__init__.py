from pydantic import BaseModel
from typing import List

from uuid import UUID


class ObjectSchema(BaseModel):
    id: UUID
    service_name: str
    app_name: str
    table_name: str


class RelationsSchema(BaseModel):
    objs: List[ObjectSchema]
