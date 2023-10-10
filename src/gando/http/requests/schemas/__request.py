from pydantic import BaseModel

from typing import Any


class AnonymousUser(BaseModel):
    id: int = None
    pk: int = None

    username: str = ''

    user_permissions: Any = None

    is_superuser: bool = False
    is_staff: bool = False
    is_authenticated: bool = False
    is_anonymous: bool = True
    is_active: bool = False

    groups: Any = None


class RequestSchema(BaseModel):
    data: dict = dict()
    query_params: dict = dict()
    method: str
    user: Any = AnonymousUser()
    headers: dict = dict()
    cookies: dict = dict()
