from gando.config import SETTINGS
from django.utils.deprecation import MiddlewareMixin


def _get_user_agent_device_key(key):
    from gando.models import UserAgentDevice

    if not key:
        return None
    try:
        obj = UserAgentDevice.objects.get(key=key)
        return obj.key
    except:
        return None


def _create_user_agent_device_key(request):
    from gando.models import UserAgentDevice, user_agent_device_key_creator
    from gando.utils.client import UADSchema

    params = UADSchema(request)
    try:
        obj = UserAgentDevice.objects.create(
            **params.model_dump()
        )
        return obj.key
    except:
        key = user_agent_device_key_creator(params)
        return key


def user_agent_device_id(request):
    if SETTINGS.USER_AGENT_DEVICE_HANDLER.HANDLING is False:
        return None

    cookie_name = SETTINGS.USER_AGENT_DEVICE_HANDLER.COOKIE_NAME
    if not hasattr(request, 'COOKIES'):
        return None

    adk = request.COOKIES.get(cookie_name)

    uad_key = _get_user_agent_device_key(adk)
    if uad_key:
        return uad_key

    uad_key = _create_user_agent_device_key(request)
    return uad_key


class UserAgentDeviceMiddleware(MiddlewareMixin):

    def process_request(self, request):
        setattr(request, 'uad', user_agent_device_id(request))

    def process_response(self, request, response):
        self.process_request(request)

        if SETTINGS.USER_AGENT_DEVICE_HANDLER.HANDLING is False:
            return response

        response.set_cookie(
            key=SETTINGS.USER_AGENT_DEVICE_HANDLER.COOKIE_NAME,
            value=request.uad,
            max_age=60 * 60 * 24 * 365,
            httponly=False,
            secure=False
        )
        return response
