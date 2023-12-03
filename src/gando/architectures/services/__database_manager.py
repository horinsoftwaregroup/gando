from gando.architectures.services import BaseService
from django.db.models import Model
from abc import abstractmethod
from pydantic import BaseModel


class BaseDataBaseManagerService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def model(self) -> Model:
        if not hasattr(self, 'model_class'):
            raise Exception('model_class not define.')
        return self.model_class

    @property
    def output_schema(self) -> BaseModel:
        if not hasattr(self, 'output_schema_class'):
            raise Exception('output_schema_class not define.')
        return self.output_schema_class

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
