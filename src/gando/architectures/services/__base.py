from abc import abstractmethod


class BaseService:
    reset_cache: bool = False

    def __init__(self, cache: bool = True, *args, **kwargs):
        self.cache: bool = cache

    @abstractmethod
    def execute(self, reset_cache=False, *args, **kwargs):
        pass
