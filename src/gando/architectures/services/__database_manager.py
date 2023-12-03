from abc import abstractmethod
from pydantic import BaseModel

from django.db.models import Model

from gando.architectures.services import BaseService


class BaseDataBaseManagerService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    @abstractmethod
    def model(self) -> Model:
        pass

    @property
    @abstractmethod
    def output_schema(self) -> BaseModel:
        pass

    def __convert_to_schema(self, obj):
        ret = self.output_schema(**obj) if obj else None
        return ret

    def execute(self, *args, **kwargs):
        rslt = super().execute(*args, **kwargs)
        ret = self.__convert_to_schema(rslt)
        return ret

    @abstractmethod
    def service_output_handler(self, *args, **kwargs):
        pass
