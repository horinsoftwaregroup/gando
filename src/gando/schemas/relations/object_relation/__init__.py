from pydantic import BaseModel
from typing import List


class Object(BaseModel):
    id: str
    service_name: str
    app_name: str
    table_name: str


class Relations(BaseModel):
    objs: List[Object]
