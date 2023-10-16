from gando.config import SETTINGS

from rest_framework.response import Response
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

    def response_context(self, data=None):
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
            tmp['messages'] = self.__messages()
            tmp['headers'] = self.get_headers()

        ret = tmp
        return ret

    def set_log_message(self, key, value):
        log = {key: value}
        self.__logs_message.append(log)

    def set_info_message(self, key, value):
        info = {key: value}
        self.__infos_message.append(info)

    def set_warning_message(self, key, value):
        warning = {key: value}
        self.__warnings_message.append(warning)

    def set_error_message(self, key, value):
        error = {key: value}
        self.__errors_message.append(error)

    def set_exception_message(self, key, value):
        exception = {key: value}
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

        if data is None:
            tmp = {'result': {'message': self.__default_message()}}

        elif isinstance(data, str):
            tmp = {'result': {'message': data}}

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

    def response(self, output_data):
        self.helper()

        data = self.response_context(output_data)
        return Response(
            data,
            status=self.get_status_code(),
            headers=self.get_headers(),
        )

    def get_host(self):
        return self.request._request._current_scheme_host

    def append_host_to_url(self, value):
        ret = f'{self.get_host()}{value}'
        return ret

    def get_media_url(self):
        from django.conf import settings

        ret = settings.MEDIA_URL
        return ret

    def convert_filename_to_url(self, file_name):
        ret = f'{self.get_media_url()}{file_name}'
        return ret

    def convert_filename_to_url_localhost(self, file_name):
        ret = f'{self.get_host()}{self.get_media_url()}{file_name}'
        return ret

    def helper(self):
        pass

    def __default_message(self):
        status_code = self.get_status_code()

        if 100 <= status_code < 200:
            msg = 'please wait...'

        elif 200 <= status_code < 300:
            msg = 'Your request has been successfully registered.'

        elif 300 <= status_code < 400:
            msg = 'The requirements for your request are not available.'

        elif 400 <= status_code < 500:
            if status_code == 400:
                msg = 'Bad Request...'

            elif status_code == 401:
                msg = {'result': {
                    'message': 'Your authentication information is not available.'}}

            elif status_code == 403:
                msg = 'You do not have access to this section.'

            elif status_code == 404:
                msg = 'There is no information about your request.'

            else:
                msg = 'There was an error in how to send the request.'

        elif 500 <= status_code:
            msg = 'The server is unable to respond to your request.'

        else:
            msg = 'Undefined.'

        return msg
