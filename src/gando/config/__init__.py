from pydantic import BaseModel as Base
from functools import lru_cache

from django.conf import settings


class Gando(Base):
    MONITOR_KEYS: list = list()
    DEBUG: bool = True
    CACHING: bool = False
    MESSAGES_RESPONSE_DISPLAYED: bool = True


@lru_cache()
def __get_settings():
    try:
        input_conf = settings.GANDO
    except:
        input_conf = {}
    try:
        input_conf['DEBUG'] = settings.DEBUG
    except:
        pass
    return Gando(**input_conf)


SETTINGS = __get_settings()
