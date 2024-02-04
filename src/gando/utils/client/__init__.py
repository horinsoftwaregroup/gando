from pydantic import BaseModel


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class UADSchema(BaseModel):
    def __init__(self, request):
        kw = {}
        if hasattr(request, 'user_agent'):
            user_agent = request.user_agent
            kw = {
                'user_id': request.user.id if request.user.is_authenticated else None,

                'user_agent_is_mobile': user_agent.is_mobile,
                'user_agent_is_tablet': user_agent.is_tablet,
                'user_agent_is_touch_capable': user_agent.is_touch_capable,
                'user_agent_is_pc': user_agent.is_pc,
                'user_agent_is_bot': user_agent.is_bot,

                'user_agent_browser_family': user_agent.browser.family,
                'user_agent_browser_version': user_agent.browser.version_string,

                'user_agent_os_family': user_agent.os.family,
                'user_agent_os_version': user_agent.os.version_string,

                'user_agent_device_family': user_agent.device.family,
                'user_agent_device_brand': user_agent.device.brand,
                'user_agent_device_model': user_agent.device.model,

                'ip': get_client_ip(request)
            }
        super().__init__(**kw)

    user_id: int | None = None
    user_agent_is_mobile: bool | None = None
    user_agent_is_tablet: bool | None = None
    user_agent_is_touch_capable: bool | None = None
    user_agent_is_pc: bool | None = None
    user_agent_is_bot: bool | None = None
    user_agent_browser_family: str | None = None
    user_agent_browser_version: str | None = None
    user_agent_os_family: str | None = None
    user_agent_os_version: str | None = None
    user_agent_device_family: str | None = None
    user_agent_device_brand: str | None = None
    user_agent_device_model: str | None = None
    ip: str | None = None
