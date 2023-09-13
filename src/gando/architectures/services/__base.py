from abc import abstractmethod


class BaseService:

    def __init__(self, cache_reset: bool = False, *args, **kwargs):
        self.cache_reset = cache_reset

    @abstractmethod
    def execute(self):
        pass
