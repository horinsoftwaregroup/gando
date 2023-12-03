from abc import abstractmethod
from pydantic import BaseModel

from django.db.models import Model

from gando.architectures.services import BaseCreatorService


class BaseGetterCreatorService(BaseCreatorService):

    def __get_or_create_db_record(self):
        try:
            obj = self.model.objects.get(**self.valid_input_data)
        except self.model.DoesNotExist:
            obj = self.model.objects.create(**self.valid_input_data)
        except Exception as exc:
            raise exc
        return obj.__dict__

    def service_output_handler(self, *args, **kwargs):
        return self.__get_or_create_db_record()

    @property
    @abstractmethod
    def valid_key_input_data_list(self) -> list:
        pass

    @property
    @abstractmethod
    def model(self) -> Model:
        pass

    @property
    @abstractmethod
    def output_schema(self) -> BaseModel:
        pass
