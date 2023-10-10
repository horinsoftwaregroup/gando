from gando.config import SETTINGS

from rest_framework.views import APIView


class BaseAPI(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._data = None

        self._logs_message = []
        self._infos_message = []
        self._warnings_message = []
        self._errors_message = []
        self._exceptions_message = []

        self._monitor: dict = dict()

        self._status_code: int | None = None

        self._headers: dict = dict()

    def response_context(self, data):
        self._data = data
        tmp = {
            'success': self._success(),
            'status_code': self.get_status_code(),
            'has_warning': self._has_warning(),
            'messages': self._messages(),
            'monitor': self._monitor,
            'data': self.validate_data(),
            'many': self._many(),
        }
        if self._debug_status:
            tmp['headers'] = self.headers

        ret = tmp
        return ret

    def set_log_message(self, key, value):
        log = {key, value}
        self._logs_message.append(log)

    def set_info_message(self, key, value):
        info = {key, value}
        self._infos_message.append(info)

    def set_warning_message(self, key, value):
        warning = {key, value}
        self._warnings_message.append(warning)

    def set_error_message(self, key, value):
        error = {key, value}
        self._errors_message.append(error)

    def set_exception_message(self, key, value):
        exception = {key, value}
        self._exceptions_message.append(exception)

    def set_headers_message(self, key, value):
        self._headers[key] = value

    def get_headers(self):
        return self._headers

    def _messages(self, ) -> dict:
        tmp = {
            'info': self._infos_message,
            'warning': self._warnings_message,
            'error': self._errors_message,

        }
        if self._debug_status:
            tmp['log'] = self._logs_message
            tmp['exception'] = self._exceptions_message

        ret = tmp
        return ret

    def _many(self):
        if isinstance(self._data, list):
            return True
        return False

    def _success(self):
        if len(self._errors_message) == 0 and len(self._exceptions_message) == 0:
            return True
        return False

    def _has_warning(self):
        if len(self._warnings_message) != 0:
            return True
        return False

    def set_status_code(self, value: int):
        self._status_code = value

    def get_status_code(self):
        return self._status_code or 200

    def set_monitor(self, key, value):
        if key in self._allowed_monitor_keys:
            self._monitor[key] = value

    @property
    def _allowed_monitor_keys(self):
        return SETTINGS.MONITOR_KEYS

    def validate_data(self):
        data = self._data

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
    def _debug_status(self):
        return SETTINGS.DEBUG
