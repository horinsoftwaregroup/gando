from gando.architectures.services import BaseDataBaseManagerService


class BaseUpdaterService(BaseDataBaseManagerService):
    def __init__(self, lockup_fields_dict, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.valid_input_data = self.__validate(**kwargs)
        self.obj_keyval = lockup_fields_dict

    @property
    def valid_key_input_data(self) -> list:
        if not hasattr(self, 'valid_key_input_data_list'):
            raise Exception('valid_key_input_data_list not define.')
        return self.valid_key_input_data_list

    def __validate(self, **kwargs):
        tmp = {}
        for k, v in kwargs.items():
            if k in self.valid_key_input_data:
                tmp[k] = v
        ret = tmp
        return ret

    def __update_db_record(self):
        try:
            obj = self.model.objects.get(**self.obj_keyval).update(**self.valid_input_data)
        except Exception as exc:
            raise exc
        return obj.__dict__

    def service_output_handler(self, *args, **kwargs):
        return self.__update_db_record()
