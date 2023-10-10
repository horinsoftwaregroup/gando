from pydantic import BaseModel
from typing import Optional
from . import MessagesSchema


class Response(BaseModel):
    success: bool = True
    headers: dict = dict()
    status_code: int = 200
    has_warning: bool = False
    monitor: dict = dict()
    messages: Optional[MessagesSchema] = MessagesSchema()
    data: dict = dict()
    many: bool = False
