from gando.config import SETTINGS

from rest_framework.views import APIView


class BaseAPI(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__data = None

        self.__logs_message = []
        self.__infos_message = []
        self.__warnings_message = []
        self.__errors_message = []
        self.__exceptions_message = []

        self.__monitor: dict = dict()

        self.__status_code: int | None = None

        self.__headers: dict = dict()

    def response_context(self, data):
        self.__data = data
        tmp = {
            'success': self.__success(),
            'status_code': self.get_status_code(),
            'has_warning': self.__has_warning(),
            'monitor': self.__monitor,
            'data': self.validate_data(),
            'many': self.__many(),
        }
        if self.__debug_status:
            tmp['messages']=self.__messages()
            tmp['headers'] = self.get_headers()

        ret = tmp
        return ret

    def set_log_message(self, key, value):
        log = {key, value}
        self.__logs_message.append(log)

    def set_info_message(self, key, value):
        info = {key, value}
        self.__infos_message.append(info)

    def set_warning_message(self, key, value):
        warning = {key, value}
        self.__warnings_message.append(warning)

    def set_error_message(self, key, value):
        error = {key, value}
        self.__errors_message.append(error)

    def set_exception_message(self, key, value):
        exception = {key, value}
        self.__exceptions_message.append(exception)

    def set_headers(self, key, value):
        self.__headers[key] = value

    def get_headers(self):
        return self.__headers

    def __messages(self, ) -> dict:
        tmp = {
            'info': self.__infos_message,
            'warning': self.__warnings_message,
            'error': self.__errors_message,

        }
        if self.__debug_status:
            tmp['log'] = self.__logs_message
            tmp['exception'] = self.__exceptions_message

        ret = tmp
        return ret

    def __many(self):
        if isinstance(self.__data, list):
            return True
        return False

    def __success(self):
        if len(self.__errors_message) == 0 and len(self.__exceptions_message) == 0:
            return True
        return False

    def __has_warning(self):
        if len(self.__warnings_message) != 0:
            return True
        return False

    def set_status_code(self, value: int):
        self.__status_code = value

    def get_status_code(self):
        return self.__status_code or 200

    def set_monitor(self, key, value):
        if key in self.__allowed_monitor_keys:
            self.__monitor[key] = value

    @property
    def __allowed_monitor_keys(self):
        return SETTINGS.MONITOR_KEYS

    def validate_data(self):
        data = self.__data

        if isinstance(data, str):
            tmp = {'result': {'str': data}}

        elif isinstance(data, list):
            tmp = {
                'count': len(data),
                'next': None,
                'previous': None,
                'results': data,
            }

        elif isinstance(data, dict):
            tmp = {'result': data}

        else:
            tmp = {'result': {}}

        ret = tmp
        return ret

    @property
    def __debug_status(self):
        return SETTINGS.DEBUG
