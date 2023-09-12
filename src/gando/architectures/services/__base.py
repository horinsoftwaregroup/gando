from abc import abstractmethod


class BaseService:
    __is_completed = False

    @abstractmethod
    def execute(self):
        pass
