from pydantic import BaseModel
from typing import Optional
from . import MessagesSchema


class Response(BaseModel):
    success: bool = True
    has_warning: bool = False
    messages: Optional[MessagesSchema] = MessagesSchema()
    monitor: dict = dict()
    data: dict = dict()
