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
