from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models


def user_agent_device_key_creator(instance):
    from hashlib import md5

    str_ = (
        f"{instance.user_agent_is_mobile}-"
        f"{instance.user_agent_is_tablet}-"
        f"{instance.user_agent_is_touch_capable}-"
        f"{instance.user_agent_is_pc}-"
        f"{instance.user_agent_is_bot}-"
        f"{instance.user_agent_browser}-"
        f"{instance.user_agent_browser_family}-"
        f"{instance.user_agent_browser_version_string}-"
        f"{instance.user_agent_os}-"
        f"{instance.user_agent_os_version_string}-"
        f"{instance.user_agent_device}-"
        f"{instance.user_agent_device_family}-"
        f"{instance.geoip}-"
        f"{instance.geoip_country_code}-"
        f"{instance.geoip_country_name}-"
        f"{instance.geoip_area_code}-"
        f"{instance.geoip_city}-"
        f"{instance.geoip_country_code3}-"
        f"{instance.geoip_dma_code}-"
        f"{instance.geoip_latitude}-"
        f"{instance.geoip_longitude}-"
        f"{instance.geoip_postal_code}-"
        f"{instance.geoip_region}-"
        f"{instance.geoip_geos_x}-"
        f"{instance.geoip_geos_y}-"
        f"{instance.geoip_time_zone}"
    )
    ret = md5(str_.encode('utf-8'))
    return ret


class UserAgentDevice(models.Model):
    user = models.ForeignKey(
        verbose_name=_('User'),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='uad',
        db_index=True,
        blank=True,
        null=True,
    )
    user_agent_is_mobile = models.IntegerField(
        verbose_name=_('Mobile'),
        blank=True,
        null=True,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
    )
    user_agent_is_tablet = models.IntegerField(
        verbose_name=_('Tablet'),
        blank=True,
        null=True,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
    )
    user_agent_is_touch_capable = models.IntegerField(
        verbose_name=_('TouchCapable'),
        blank=True,
        null=True,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
    )
    user_agent_is_pc = models.IntegerField(
        verbose_name=_('PC'),
        blank=True,
        null=True,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
    )
    user_agent_is_bot = models.IntegerField(
        verbose_name=_('Bot'),
        blank=True,
        null=True,
        choices=(
            (0, 'No'),
            (1, 'Yes'),
        ),
    )
    user_agent_browser = models.CharField(
        verbose_name=_('Browser'),
        blank=True,
        null=True,
        max_length=255,
    )
    user_agent_browser_family = models.CharField(
        verbose_name=_('BrowserFamily'),
        blank=True,
        null=True,
        max_length=255,
    )
    user_agent_browser_version_string = models.CharField(
        verbose_name=_('BrowserVersion'),
        blank=True,
        null=True,
        max_length=255,
    )
    user_agent_os = models.CharField(
        verbose_name=_('OS'),
        blank=True,
        null=True,
        max_length=255,
    )
    user_agent_os_version_string = models.CharField(
        verbose_name=_('OSVersion'),
        blank=True,
        null=True,
        max_length=255,
    )
    user_agent_device = models.CharField(
        verbose_name=_('Device'),
        blank=True,
        null=True,
        max_length=255,
    )
    user_agent_device_family = models.CharField(
        verbose_name=_('DeviceFamily'),
        blank=True,
        null=True,
        max_length=255,
    )
    # geoip
    geoip_ip = models.CharField(
        verbose_name=_('IP'),
        max_length=255,
        blank=True,
        null=True,
    )
    geoip_country_code = models.CharField(
        verbose_name=_('CountryCode'),
        max_length=255,
        blank=True,
        null=True,
    )
    geoip_country_name = models.CharField(
        verbose_name=_('CountryName'),
        max_length=255,
        blank=True,
        null=True,
    )
    geoip_area_code = models.IntegerField(
        verbose_name=_('AreaCode'),
        blank=True,
        null=True,
    )
    geoip_city = models.CharField(
        verbose_name=_('City'),
        max_length=255,
        blank=True,
        null=True,
    )
    geoip_country_code3 = models.CharField(
        verbose_name=_('CountryCode3'),
        max_length=255,
        blank=True,
        null=True,
    )
    geoip_dma_code = models.IntegerField(
        verbose_name=_('DMACode'),
        blank=True,
        null=True,
    )
    geoip_latitude = models.FloatField(
        verbose_name=_('Latitude'),
        blank=True,
        null=True,
    )
    geoip_longitude = models.FloatField(
        verbose_name=_('Longitude'),
        blank=True,
        null=True,
    )
    geoip_postal_code = models.CharField(
        verbose_name=_('PostalCode'),
        max_length=255,
        blank=True,
        null=True,
    )
    geoip_region = models.CharField(
        verbose_name=_('Region'),
        max_length=255,
        blank=True,
        null=True,
    )
    geoip_time_zone = models.CharField(
        verbose_name=_('TimeZone'),
        max_length=255,
        blank=True,
        null=True,
    )
    geoip_geos_x = models.FloatField(
        verbose_name=_('GEOS.x'),
        blank=True,
        null=True,
    )
    geoip_geos_y = models.FloatField(
        verbose_name=_('GEOS.y'),
        blank=True,
        null=True,
    )
    created_dt = models.DateTimeField(
        verbose_name=_('Created Datetime'),
        auto_now_add=True,
        db_index=True,
    )
    key = models.CharField(
        verbose_name=_('key'),
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
        unique=True,
    )

    def __str__(self):
        return f'{self.key}'

    def save(self, **kwargs):
        self.key = user_agent_device_key_creator(self)
        super().save(**kwargs)

    class Meta:
        verbose_name = _('UserAgentDevice')
        verbose_name_plural = _('UserAgentDevices')
