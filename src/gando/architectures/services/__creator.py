from abc import abstractmethod

from gando.architectures.services import BaseDataBaseManagerService


class BaseCreatorService(BaseDataBaseManagerService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.valid_input_data = self.__validate(**kwargs)

    @abstractmethod
    def valid_key_input_data_list(self):
        return []

    def __validate(self, **kwargs):
        tmp = {}
        for k, v in kwargs.items():
            if k in self.valid_key_input_data_list():
                tmp[k] = v
        ret = tmp
        return ret

    def __create_db_record(self):
        try:
            obj = self.model.objects.create(**self.valid_input_data)
        except Exception as exc:
            raise exc
        return obj.__dict__

    def service_output_handler(self, *args, **kwargs):
        return self.__create_db_record()
