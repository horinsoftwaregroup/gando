from django.contrib import admin

from gando.models import UserAgentDevice


@admin.register(UserAgentDevice)
class UserAgentDeviceModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'key',

        'user',

        'created_dt',

        'ip',

        'user_agent_is_mobile',
        'user_agent_is_tablet',
        'user_agent_is_touch_capable',
        'user_agent_is_pc',
        'user_agent_is_bot',

        'user_agent_browser_family',
        'user_agent_browser_version',

        'user_agent_os_family',
        'user_agent_os_version',

        'user_agent_device_family',
        'user_agent_device_brand',
        'user_agent_device_model',
    )
    list_display_links = (
        'id',

        'key',

        'user',

        'created_dt',

        'ip',

        'user_agent_is_mobile',
        'user_agent_is_tablet',
        'user_agent_is_touch_capable',
        'user_agent_is_pc',
        'user_agent_is_bot',

        'user_agent_browser_family',
        'user_agent_browser_version',

        'user_agent_os_family',
        'user_agent_os_version',

        'user_agent_device_family',
        'user_agent_device_brand',
        'user_agent_device_model',
    )
    search_fields = (
        'id',
        'user__id',
        'ip',

        'key',
    )
    list_filter = (
        'user_agent_is_mobile',
        'user_agent_is_tablet',
        'user_agent_is_touch_capable',
        'user_agent_is_pc',
        'user_agent_is_bot',

        'user_agent_browser_family',
        'user_agent_browser_version',

        'user_agent_os_family',
        'user_agent_os_version',

        'user_agent_device_family',
        'user_agent_device_brand',
        'user_agent_device_model',
    )
    readonly_fields = ('id', 'created_dt', 'key',)
    fieldsets = [
        ('Base Info', {'fields': [
            'id',
            'user',
            'key',
            'ip',
            'created_dt',
        ]}),
        ('UserAgent', {'fields': [
            'user_agent_is_mobile',
            'user_agent_is_tablet',
            'user_agent_is_touch_capable',
            'user_agent_is_pc',
            'user_agent_is_bot',

            'user_agent_browser_family',
            'user_agent_browser_version',

            'user_agent_os_family',
            'user_agent_os_version',

            'user_agent_device_family',
            'user_agent_device_brand',
            'user_agent_device_model',
        ]}),
    ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
