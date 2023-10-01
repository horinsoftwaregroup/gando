from abc import abstractmethod
from types import NoneType
from pydantic import BaseModel

from django.core.cache import cache as djcache

from gando.config import SETTINGS


class CacheConfig(BaseModel):
    cache_prefix_key: str | None = None
    cache_suffix_key: str | None = None
    cache_middle_separator_key: str | None = None
    cache: bool | None = None
    cache_timeout: int | None = None
    cache_unique_key: str | tuple | list | set | None = None


class BaseService:
    """
    - Config:
        - type:
            - class

        - attrs:
            - cache:
                - type:
                    - bool
                - descriptions:
                    - Using this variable,
                    you can activate or deactivate the service's automatic caching system.
                    The default mode is disabled.

            - cache_key:
                - type:
                    - str or tuple or list or set
                - descriptions:
                    - You can choose a variable or a combination of a number of variables as
                    a unique key for caching.
                    If there is no such key,
                    the same name is selected as the unique key.

            - cache_prefix_key:
                - type:
                    - str

            - cache_middle_separator_key:
                - type:
                    - str

            - cache_suffix_key:
                - type:
                    - str

            - cache_timeout:
                - type:
                    - int or None
    """

    def __init__(self, *args, **kwargs):
        self.__input_cache_config: CacheConfig = CacheConfig(**kwargs)

    def execute(self, reset_cache=False, *args, **kwargs):
        if SETTINGS.CACHING and self.cache:
            if reset_cache:
                output = self.service_output_handler(*args, **kwargs)
            else:
                tmp = djcache.get(key=self.cache_unique_key())
                if tmp is None:
                    tmp = self.service_output_handler(self, *args, **kwargs)
                output = tmp
            djcache.set(key=self.cache_unique_key(), value=output)
        else:
            output = self.service_output_handler(self, *args, **kwargs)

        ret = output
        return ret

    @abstractmethod
    def service_output_handler(self, *args, **kwargs):
        pass

    @property
    def cache_prefix_key(self):
        if self.__input_cache_config.cache_prefix_key is not None:
            return self.__input_cache_config.cache_prefix_key

        if (
            hasattr(self, 'Config') and
            hasattr(self.Config, 'cache_prefix_key') and
            isinstance(self.Config.cache_prefix_key, str)
        ):
            return self.Config.cache_prefix_key

        return ''

    @property
    def cache_suffix_key(self):
        if self.__input_cache_config.cache_suffix_key is not None:
            return self.__input_cache_config.cache_suffix_key

        if (
            hasattr(self, 'Config') and
            hasattr(self.Config, 'cache_suffix_key') and
            isinstance(self.Config.cache_suffix_key, str)
        ):
            return self.Config.cache_suffix_key

        return ''

    @property
    def cache_middle_separator_key(self):
        if self.__input_cache_config.cache_middle_separator_key is not None:
            return self.__input_cache_config.cache_middle_separator_key

        if (
            hasattr(self, 'Config') and
            hasattr(self.Config, 'cache_middle_separator_key') and
            isinstance(self.Config.cache_middle_separator_key, str)
        ):
            return self.Config.cache_middle_separator_key

        return ''

    @property
    def cache(self):
        if self.__input_cache_config.cache is not None:
            return self.__input_cache_config.cache

        if (
            hasattr(self, 'Config') and
            hasattr(self.Config, 'cache') and
            isinstance(self.Config.cache, bool)
        ):
            return self.Config.cache

        return False

    @property
    def cache_timeout(self):
        if self.__input_cache_config.cache_timeout is not None:
            return self.__input_cache_config.cache_timeout

        ret = 5
        if hasattr(self, 'Config') and hasattr(self.Config, 'cache_timeout'):
            if isinstance(self.Config.cache_timeout, int) or isinstance(self.Config.cache_timeout, NoneType):
                ret = self.Config.cache_timeout

        return ret

    def cache_unique_key(self):
        if self.__input_cache_config.cache_unique_key is not None:
            return self.__input_cache_config.cache_unique_key

        if hasattr(self, 'Config') and hasattr(self.Config, 'cache_key'):
            keys = []
            if isinstance(self.Config.cache_key, str):
                keys = [self.Config.cache_key]

            elif (
                isinstance(self.Config.cache_key, tuple) or
                isinstance(self.Config.cache_key, list) or
                isinstance(self.Config.cache_key, set)
            ):
                keys = [i for i in self.Config.cache_key]

            else:
                pass

            ret = (
                self.cache_prefix_key +
                self.cache_middle_separator_key.join(
                    str(
                        getattr(self, i) if hasattr(self, i) else i.upper()
                    ) for i in keys
                ) +
                self.cache_suffix_key
            )
            return ret

        return ''
