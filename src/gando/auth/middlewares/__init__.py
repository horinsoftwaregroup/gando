from django.utils.functional import SimpleLazyObject
from gando.config import SETTINGS
from django.utils.deprecation import MiddlewareMixin


def _get_user_agent_device_id(key):
    from gando.models import UserAgentDevice

    try:
        obj = UserAgentDevice.objects.get(key=key)
        return obj.id
    except:
        return None


def _create_user_agent_device_id(request):
    from gando.models import UserAgentDevice
    from gando.utils.client import get_user_agent_device_info

    params = get_user_agent_device_info(request)
    obj = UserAgentDevice.objects.create(
        **params
    )
    return obj.id


def user_agent_device_id(request):
    if SETTINGS.USER_AGENT_DEVICE_HANDLER.HANDLING is False:
        return None

    cookie_name = SETTINGS.USER_AGENT_DEVICE_HANDLER.COOKIE_NAME
    if not hasattr(request, 'COOKIES'):
        return None

    adk = request.COOKIES.get(cookie_name)
    if not adk:
        return None

    uad_id = _get_user_agent_device_id(adk)
    if uad_id:
        return uad_id

    uad_id = _create_user_agent_device_id(request)
    return uad_id


class UserAgentDeviceMiddleware(MiddlewareMixin):

    def process_request(self, request):
        setattr(request, 'uad', user_agent_device_id(request))

    def process_response(self, request, response):
        self.process_request(request)
        response.set_cookie(
            key=SETTINGS.USER_AGENT_DEVICE_HANDLER.COOKIE_NAME,
            value=request.uad,
            max_age=100000,
            httponly=True,
            secure=True
        )
        return response
