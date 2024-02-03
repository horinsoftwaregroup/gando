def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    if not hasattr(request, 'user_agent'):
        return {}

    user_agent = request.user_agent
    ret = {
        'user_agent_is_mobile': user_agent.is_mobile,
        'user_agent_is_tablet': user_agent.is_tablet,
        'user_agent_is_touch_capable': user_agent.is_touch_capable,
        'user_agent_is_pc': user_agent.is_pc,
        'user_agent_is_bot': user_agent.is_bot,
        'user_agent_browser': user_agent.browser,
        'user_agent_browser_family': user_agent.browser.family,
        'user_agent_browser_version_string': user_agent.browser.version_string,
        'user_agent_os': user_agent.os,
        'user_agent_os_version_string': user_agent.os.version_string,
        'user_agent_device': user_agent.device,
        'user_agent_device_family': user_agent.device.family,
    }
    return ret


def get_user_geoip(request):
    from django.contrib.gis.geoip2 import GeoIP2

    g = GeoIP2()

    ip = get_client_ip(request)
    geoip = ip

    g_country = g.country(ip)
    geoip_country_code = g_country.get('country_code')
    geoip_country_name = g_country.get('country_name')

    g_city = g.city(ip)
    geoip_area_code = g_city.get('area_code')
    geoip_city = g_city.get('city')
    geoip_country_code3 = g_city.get('country_code3')
    geoip_dma_code = g_city.get('dma_code')
    geoip_postal_code = g_city.get('postal_code')
    geoip_region = g_city.get('region')
    geoip_time_zone = g_city.get('time_zone')

    g_lat_long = g.lat_lon(ip)
    geoip_latitude = g_lat_long.get('latitude')
    geoip_longitude = g_lat_long.get('longitude')

    g_geos = g.geos(ip)
    geoip_geos_x = g_geos.x
    geoip_geos_y = g_geos.y

    ret = {
        'geoip': geoip,
        'geoip_country_code': geoip_country_code,
        'geoip_country_name': geoip_country_name,
        'geoip_area_code': geoip_area_code,
        'geoip_city': geoip_city,
        'geoip_country_code3': geoip_country_code3,
        'geoip_dma_code': geoip_dma_code,
        'geoip_latitude': geoip_latitude,
        'geoip_longitude': geoip_longitude,
        'geoip_postal_code': geoip_postal_code,
        'geoip_region': geoip_region,
        'geoip_geos_x': geoip_geos_x,
        'geoip_geos_y': geoip_geos_y,
        'geoip_time_zone': geoip_time_zone,
    }
    return ret


def get_user_agent_device_info(request):
    tmp = get_user_agent(request)
    tmp.update(get_user_geoip(request))
    ret = tmp
    return ret
