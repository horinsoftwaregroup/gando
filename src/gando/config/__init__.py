from pydantic import BaseModel as Base
from functools import lru_cache

from django.conf import settings


class ExceptionHandlerObject(Base):
    HANDLING: bool = False
    COMMUNICATION_WITH_SOFTWARE_SUPPORT: str = None


class UserAgentDeviceHandlerObject(Base):
    HANDLING: bool = False
    COOKIE_NAME: str = 'uad'


class Gando(Base):
    MONITOR_KEYS: list = list()
    DEBUG: bool = True
    CACHING: bool = False
    MESSAGES_RESPONSE_DISPLAYED: bool = True
    MONITOR: dict = dict()
    EXCEPTION_HANDLER: ExceptionHandlerObject = ExceptionHandlerObject()
    PASTE_TO_REQUEST: dict = dict()
    USER_AGENT_DEVICE_HANDLER: UserAgentDeviceHandlerObject = UserAgentDeviceHandlerObject()


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

    input_conf['EXCEPTION_HANDLER'] = (
        ExceptionHandlerObject(**input_conf['EXCEPTION_HANDLER'])
        if 'EXCEPTION_HANDLER' in input_conf
        else ExceptionHandlerObject()
    )
    input_conf['USER_AGENT_DEVICE_HANDLER'] = (
        UserAgentDeviceHandlerObject(**input_conf['USER_AGENT_DEVICE_HANDLER'])
        if 'USER_AGENT_DEVICE_HANDLER' in input_conf
        else UserAgentDeviceHandlerObject()
    )

    return Gando(**input_conf)


SETTINGS = __get_settings()
