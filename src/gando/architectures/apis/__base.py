from pydantic import BaseModel
from typing import Any

from gando.http.responses.string_messages import (
    InfoStringMessage,
    ErrorStringMessage,
    WarningStringMessage,
    LogStringMessage,
    ExceptionStringMessage,
)
from gando.config import SETTINGS

from rest_framework.exceptions import ErrorDetail
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
        self.__cookies_for_set: list = list()
        self.__cookies_for_delete: list = list()

        self.__content_type: str | None = None
        self.__exception_status: bool = False

    def finalize_response(self, request, response, *args, **kwargs):
        if isinstance(response, Response):
            self.helper()

            tmp = response.template_name if hasattr(response, 'template_name') else None
            template_name = tmp

            tmp = response.headers if hasattr(response, 'headers') else None
            headers = self.get_headers(tmp)

            tmp = response.exception if hasattr(response, 'exception') else None
            exception = self.get_exception_status(tmp)

            tmp = response.content_type if hasattr(response, 'content_type') else None
            content_type = tmp

            tmp = response.status_code if hasattr(response, 'status_code') else None
            status_code = self.get_status_code(tmp)

            tmp = response.data if hasattr(response, 'data') else None
            data = self.response_context(tmp)

            response = Response(
                data=data,
                status=status_code,
                template_name=template_name,
                headers=headers,
                exception=exception,
                content_type=content_type,
            )

            if self.__cookies_for_delete:
                for i in self.__cookies_for_delete:
                    response.delete_cookie(i)

            if self.__cookies_for_set:
                for i in self.__cookies_for_set:
                    response.set_cookie(**i)

        return super().finalize_response(request, response, *args, **kwargs)

    def response_context(self, data=None):
        self.__data = self.__set_messages_from_data(data)

        status_code = self.get_status_code()
        content_type = self.get_content_type()
        data = self.validate_data()
        many = self.__many()

        monitor = self.__monitor

        has_warning = self.__has_warning()
        exception_status = self.get_exception_status()

        messages = self.__messages()

        success = self.__success()

        headers = self.get_headers()

        tmp = {
            'success': success,

            'status_code': status_code,

            'has_warning': has_warning,
            'exception_status': exception_status,

            # 'content_type': content_type,

            'messages': messages,

            'monitor': monitor,
            'many': many,
            'data': data,
        }
        if self.__debug_status:
            # tmp['headers'] = headers
            pass

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

    def get_headers(self, value: dict = None):
        if value:
            for k, v in value.items():
                self.set_headers(k, v)
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
        if (
            isinstance(self.__data, dict) and
            'count' in self.__data and
            'next' in self.__data and
            'previous' in self.__data and
            'results' in self.__data
        ):
            return True
        return False

    def __success(self):
        if len(self.__errors_message) == 0 and len(self.__exceptions_message) == 0 and not self.__exception_status:
            return True
        return False

    def __has_warning(self):
        if len(self.__warnings_message) != 0:
            return True
        return False

    def set_status_code(self, value: int):
        self.__status_code = value

    def get_status_code(self, value: int = None):
        if value and 100 <= value < 600 and value != 200:
            self.set_status_code(value)

        return self.__status_code or 200

    def set_content_type(self, value: str):
        self.__content_type = value

    def get_content_type(self, value: str = None):
        if value:
            self.set_content_type(value)

        return self.__content_type

    def set_exception_status(self, value: bool):
        self.__exception_status = value

    def get_exception_status(self, value: bool = None):
        if value is not None:
            self.set_exception_status(value)

        return self.__exception_status

    def set_monitor(self, key, value):
        if key in self.__allowed_monitor_keys:
            self.__monitor[key] = value

    @property
    def __allowed_monitor_keys(self):
        return SETTINGS.MONITOR_KEYS

    def validate_data(self):
        data = self.__data

        if data is None:
            self.__set_default_message()
            tmp = {'result': {}}

        elif isinstance(data, str) or issubclass(type(data), str):
            data = self.__set_dynamic_message(data)
            tmp = {'result': {'string': data} if data else {}}

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

    def response(self, output_data=None):
        data = output_data
        rsp = Response(
            data,
            status=self.get_status_code(),
            headers=self.get_headers(),
        )

        return rsp

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

    def __set_default_message(self):
        status_code = self.get_status_code()

        if 100 <= status_code < 200:
            self.set_warning_message('status_code_1xx', self.__default_message())

        elif 200 <= status_code < 300:
            self.set_info_message('status_code_2xx', self.__default_message())

        elif 300 <= status_code < 400:
            self.set_error_message('status_code_3xx', self.__default_message())

        elif 400 <= status_code < 500:
            self.set_error_message('status_code_4xx', self.__default_message())

        elif 500 <= status_code:
            self.set_error_message('status_code_5xx', self.__default_message())

        else:
            self.set_error_message('status_code_xxx', self.__default_message())

    def __set_messages_from_data(self, data):
        if isinstance(data, str) or issubclass(type(data), str):
            return self.__set_dynamic_message(data)

        if isinstance(data, list):
            tmp = []
            for i in data:
                rslt = self.__set_messages_from_data(i)
                if rslt:
                    tmp.append(rslt)

            ret = tmp
            return ret

        if isinstance(data, dict):
            tmp = {}
            for k, v in data.items():
                rslt = self.__set_messages_from_data(v)
                if rslt:
                    tmp[k] = v

            ret = tmp
            return ret

        return data

    def __set_dynamic_message(self, value):
        if isinstance(value, InfoStringMessage):
            self.set_info_message(key=value.code, value=value)
            return None
        if isinstance(value, ErrorStringMessage) or isinstance(value, ErrorDetail):
            self.set_error_message(key=value.code, value=value)
            return None
        if isinstance(value, WarningStringMessage):
            self.set_warning_message(key=value.code, value=value)
            return None
        if isinstance(value, LogStringMessage):
            self.set_log_message(key=value.code, value=value)
            return None
        if isinstance(value, ExceptionStringMessage):
            self.set_exception_message(key=value.code, value=value)
            return None

        return value

    class Cookie(BaseModel):
        key: str
        value: Any = ""
        max_age: Any = None
        expires: Any = None
        path: Any = "/"
        domain: Any = None
        secure: Any = False
        httponly: Any = False
        samesite: Any = None

    def cookie_getter(self, key: str):
        ret = self.request.COOKIES.get(key)
        return ret

    def cookie_setter(self, key: str, **kwargs):
        ret = self.__cookies_for_set.append(self.Cookie(key=key, **kwargs).model_dump())
        return ret

    def cookie_deleter(self, key: str):
        ret = self.__cookies_for_delete.append(key)
        return ret
