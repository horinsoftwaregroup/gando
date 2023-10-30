from pydantic import BaseModel as Base
from functools import lru_cache

from django.conf import settings


class Gando(Base):
    MONITOR_KEYS: list = list()
    DEBUG: bool = True
    CACHING: bool = False


@lru_cache()
def __get_settings():
    input_conf = settings.GANDO or {}
    input_conf['DEBUG'] = settings.DEBUG
    return Gando(**input_conf)


SETTINGS = __get_settings()
