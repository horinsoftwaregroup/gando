from django.contrib import admin

from gando.models import UserAgentDevice


@admin.register(UserAgentDevice)
class UserAgentDeviceModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'key',

        'user',

        'created_dt',

        'geoip_ip',
        'geoip_country_code',
        'geoip_country_name',
        'geoip_area_code',
        'geoip_city',
        'geoip_country_code3',
        'geoip_dma_code',
        'geoip_latitude',
        'geoip_longitude',
        'geoip_postal_code',
        'geoip_region',
        'geoip_time_zone',
        'geoip_geos_x',
        'geoip_geos_y',

        'user_agent_is_mobile',
        'user_agent_is_tablet',
        'user_agent_is_touch_capable',
        'user_agent_is_pc',
        'user_agent_is_bot',
        'user_agent_browser',
        'user_agent_browser_family',
        'user_agent_browser_version_string',
        'user_agent_os',
        'user_agent_os_version_string',
        'user_agent_device',
        'user_agent_device_family',
    )
    list_display_links = (

    )
    search_fields = (
        'id',
        'user__id',
        'geoip_ip',
        'geoip_country_code',
        'geoip_country_name',
        'geoip_area_code',
        'geoip_city',
        'geoip_country_code3',
        'geoip_dma_code',
        'geoip_latitude',
        'geoip_longitude',
        'geoip_postal_code',
        'geoip_region',
        'geoip_time_zone',
        'geoip_geos_x',
        'geoip_geos_y',
        'created_dt',
        'key',
    )
    list_filter = (
        'user_agent_is_mobile',
        'user_agent_is_tablet',
        'user_agent_is_touch_capable',
        'user_agent_is_pc',
        'user_agent_is_bot',
        'user_agent_browser',
        'user_agent_browser_family',
        'user_agent_browser_version_string',
        'user_agent_os',
        'user_agent_os_version_string',
        'user_agent_device',
        'user_agent_device_family',
    )
    readonly_fields = ('id', 'created_dt', 'key',)
    fieldsets = [
        ('Base Info', {'fields': [
            'id',
            'user',
            'key',
            'created_dt',
        ]}),
        ('UserAgent', {'fields': [
            'user_agent_is_mobile',
            'user_agent_is_tablet',
            'user_agent_is_touch_capable',
            'user_agent_is_pc',
            'user_agent_is_bot',
            'user_agent_browser',
            'user_agent_browser_family',
            'user_agent_browser_version_string',
            'user_agent_os',
            'user_agent_os_version_string',
            'user_agent_device',
            'user_agent_device_family',
        ]}),
        ('GeoIP', {'fields': [
            'geoip_ip',
            'geoip_country_code',
            'geoip_country_name',
            'geoip_area_code',
            'geoip_city',
            'geoip_country_code3',
            'geoip_dma_code',
            'geoip_latitude',
            'geoip_longitude',
            'geoip_postal_code',
            'geoip_region',
            'geoip_time_zone',
            'geoip_geos_x',
            'geoip_geos_y',
        ]}),
    ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
