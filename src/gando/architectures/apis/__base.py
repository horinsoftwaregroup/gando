from inspect import currentframe, getframeinfo
from pydantic import BaseModel
from typing import Any
import importlib

from gando.http.responses.string_messages import (
    InfoStringMessage,
    ErrorStringMessage,
    WarningStringMessage,
    LogStringMessage,
    ExceptionStringMessage,
)
from gando.utils.exceptions import PassException
from gando.utils.messages import (
    DefaultResponse100FailMessage,
    DefaultResponse200SuccessMessage,
    DefaultResponse201SuccessMessage,
    DefaultResponse300FailMessage,
    DefaultResponse400FailMessage,
    DefaultResponse401FailMessage,
    DefaultResponse403FailMessage,
    DefaultResponse404FailMessage,
    DefaultResponse421FailMessage,
    DefaultResponse500FailMessage,
)
from gando.config import SETTINGS

from rest_framework.exceptions import ErrorDetail
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView as DRFGCreateAPIView,
    ListAPIView as DRFGListAPIView,
    RetrieveAPIView as DRFGRetrieveAPIView,
    UpdateAPIView as DRFGUpdateAPIView,
    DestroyAPIView as DRFGDestroyAPIView,
)
from gando.http.api_exceptions import (
    EnduserResponseAPIMessage,
    DeveloperResponseAPIMessage,

    DeveloperExceptionResponseAPIMessage,
    DeveloperErrorResponseAPIMessage,
    DeveloperWarningResponseAPIMessage,
    EnduserFailResponseAPIMessage,
    EnduserErrorResponseAPIMessage,
    EnduserWarningResponseAPIMessage,
)


def _valid_user(user_id, request):
    from django.contrib.auth import get_user_model

    try:
        obj = get_user_model().objects.get(id=request.user.id)
        obj_id = obj.id if isinstance(obj.id, int) else str(obj.id)
        if obj_id == user_id:
            return True
        return False
    except:
        return False


class BaseAPI(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__messenger = []

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

    def __paste_to_request_func_loader(self, f, request, *args, **kwargs):
        try:
            mod_name, func_name = f.rsplit('.', 1)
            mod = importlib.import_module(mod_name)
            func = getattr(mod, func_name)

            return func(request=request, *args, **kwargs)
        except PassException as exc:
            frame_info = getframeinfo(currentframe())
            self.set_log_message(
                key='pass',
                value=f"message:{exc.args[0]}, "
                      f"file_name: {frame_info.filename}, "
                      f"line_number: {frame_info.lineno}")
            return None

    def paste_to_request_func_loader_play(self, request, *args, **kwargs):
        for key, f in SETTINGS.PASTE_TO_REQUEST.items():
            rslt = self.__paste_to_request_func_loader(f, request, *args, **kwargs)
            if rslt:
                setattr(request, key, rslt)

        return request

    def initialize_request(self, request, *args, **kwargs):

        request_ = super().initialize_request(request, *args, **kwargs)
        rslt = self.paste_to_request_func_loader_play(request_)
        ret = rslt
        return ret

    def handle_exception(self, exc):

        if isinstance(exc, DeveloperResponseAPIMessage):
            if isinstance(exc, DeveloperErrorResponseAPIMessage):
                self.set_status_code(exc.status_code)
                self.set_error_message(key=exc.code, value=exc.message)

            elif isinstance(exc, DeveloperExceptionResponseAPIMessage):
                self.set_status_code(exc.status_code)
                self.set_exception_message(key=exc.code, value=exc.message)

            elif isinstance(exc, DeveloperWarningResponseAPIMessage):
                self.set_status_code(exc.status_code)
                self.set_warning_message(key=exc.code, value=exc.message)

        if isinstance(exc, EnduserResponseAPIMessage):
            if isinstance(exc, EnduserErrorResponseAPIMessage):
                self.set_status_code(exc.status_code)
                self.add_error_message_to_messenger(code=exc.code, message=exc.message)

            elif isinstance(exc, EnduserFailResponseAPIMessage):
                self.set_status_code(exc.status_code)
                self.add_fail_message_to_messenger(code=exc.code, message=exc.message)

            elif isinstance(exc, EnduserWarningResponseAPIMessage):
                self.set_status_code(exc.status_code)
                self.add_warning_message_to_messenger(code=exc.code, message=exc.message)

        if SETTINGS.EXCEPTION_HANDLER.HANDLING:
            return self._handle_exception_gando_handling_true(exc)
        return self._handle_exception_gando_handling_false(exc)

    def _handle_exception_gando_handling_true(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)

        if response is None:
            response = Response()

        self.set_exception_message(
            key='unexpectedError',
            value=exc.args
        )
        self.set_error_message(
            key='unexpectedError',
            value=(
                "An unexpected error has occurred based on your request type.\n"
                "Please do not repeat this request without changing your request.\n"
                "Be sure to read the documents on how to use this service correctly.\n"
                "In any case, discuss the issue with software support.\n"
            )
        )
        self.set_warning_message(
            key='unexpectedError',
            value='Please discuss this matter with software support.',
        )
        if SETTINGS.EXCEPTION_HANDLER.COMMUNICATION_WITH_SOFTWARE_SUPPORT:
            self.set_info_message(
                key='unexpectedError',
                value=(
                    f"Please share this problem with our technical experts"
                    f" at the Email address "
                    f"'{SETTINGS.EXCEPTION_HANDLER.COMMUNICATION_WITH_SOFTWARE_SUPPORT}'."
                ),
            )
        self.set_status_code(421)
        response.exception = True
        return response

    def _handle_exception_gando_handling_false(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)

        if response is None:
            self.raise_uncaught_exception(exc)

        response.exception = True
        return response

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

            'monitor': self.monitor_play(monitor),

            'messenger': self.__messenger,

            'many': many,
            'data': data,
        }
        if self.__debug_status:
            # tmp['headers'] = headers
            pass
        if self.__messages_response_displayed:
            tmp['development_messages'] = messages

        ret = tmp
        return ret

    def __add_to_messenger(self, message, code, type_):
        self.__messenger.append(
            {
                'type': type_,
                'code': code,
                'message': message,
            }
        )

    def add_fail_message_to_messenger(self, message, code):
        self.__add_to_messenger(
            message=message,
            code=code,
            type_='FAIL',
        )

    def add_error_message_to_messenger(self, message, code):
        self.__add_to_messenger(
            message=message,
            code=code,
            type_='ERROR',
        )

    def add_warning_message_to_messenger(self, message, code):
        self.__add_to_messenger(
            message=message,
            code=code,
            type_='WARNING',
        )

    def add_success_message_to_messenger(self, message, code):
        self.__add_to_messenger(
            message=message,
            code=code,
            type_='SUCCESS',
        )

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

    def __fail_message_messenger(self):
        for msg in self.__messenger:
            if msg.get('type', '') == 'FAIL' or msg.get('type', '') == 'ERROR':
                return True
        return False

    def __warning_message_messenger(self):
        for msg in self.__messenger:
            if msg.get('type', '') == 'WARNING':
                return True
        return False

    def __success(self):
        if (
            len(self.__errors_message) == 0 and
            len(self.__exceptions_message) == 0 and
            not self.__exception_status and
            not self.__fail_message_messenger()
        ):
            return True
        return False

    def __has_warning(self):
        if len(self.__warnings_message) != 0 and self.__warning_message_messenger():
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

    def __monitor_func_loader(self, f, *args, **kwargs):
        try:
            mod_name, func_name = f.rsplit('.', 1)
            mod = importlib.import_module(mod_name)
            func = getattr(mod, func_name)

            return func(request=self.request, *args, **kwargs)
        except PassException as exc:
            frame_info = getframeinfo(currentframe())
            self.set_log_message(
                key='pass',
                value=f"message:{exc.args[0]}, "
                      f"file_name: {frame_info.filename}, "
                      f"line_number: {frame_info.lineno}")
            return None

    def monitor_play(self, monitor=None, *args, **kwargs):
        monitor = monitor or {}
        for key, f in SETTINGS.MONITOR.items():
            monitor[key] = self.__monitor_func_loader(f, *args, **kwargs)

        return monitor

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

    @property
    def __messages_response_displayed(self):
        return SETTINGS.MESSAGES_RESPONSE_DISPLAYED

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

    @staticmethod
    def get_media_url():
        from django.conf import settings

        ret = settings.MEDIA_URL
        return ret

    def convert_filename_to_url(self, file_name):
        if file_name is None:
            return None
        ret = f'{self.get_media_url()}{file_name}'
        return ret

    def convert_filename_to_url_localhost(self, file_name):
        if file_name is None:
            return None
        ret = f'{self.get_host()}{self.get_media_url()}{file_name}'
        return ret

    def helper(self):
        pass

    def __default_message(self):
        status_code = self.get_status_code()

        if 100 <= status_code < 200:
            msg = 'please wait...'

        elif 200 <= status_code < 300:
            if status_code == 201:
                msg = 'The desired object was created correctly.'
            else:
                msg = 'Your request has been successfully registered.'

        elif 300 <= status_code < 400:
            msg = 'The requirements for your request are not available.'

        elif 400 <= status_code < 500:
            if status_code == 400:
                msg = 'Bad Request...'

            elif status_code == 401:
                msg = 'Your authentication information is not available.'

            elif status_code == 403:
                msg = 'You do not have access to this section.'

            elif status_code == 404:
                msg = 'There is no information about your request.'

            elif status_code == 421:
                msg = (
                    "An unexpected error has occurred based on your request type.\n"
                    "Please do not repeat this request without changing your request.\n"
                    "Be sure to read the documents on how to use this service correctly.\n"
                    "In any case, discuss the issue with software support.\n"
                )

            else:
                msg = 'There was an error in how to send the request.'

        elif 500 <= status_code:
            msg = 'The server is unable to respond to your request.'

        else:
            msg = 'Undefined.'

        return msg

    def __default_messenger_message_adder(self):
        status_code = self.get_status_code()

        if 100 <= status_code < 200:
            self.__add_to_messenger(
                message=DefaultResponse100FailMessage.message,
                code=DefaultResponse100FailMessage.code,
                type_=DefaultResponse100FailMessage.type,
            )

        elif 200 <= status_code < 300:
            if status_code == 201:
                self.__add_to_messenger(
                    message=DefaultResponse201SuccessMessage.message,
                    code=DefaultResponse201SuccessMessage.code,
                    type_=DefaultResponse201SuccessMessage.type,
                )
            else:
                self.__add_to_messenger(
                    message=DefaultResponse200SuccessMessage.message,
                    code=DefaultResponse200SuccessMessage.code,
                    type_=DefaultResponse200SuccessMessage.type,
                )

        elif 300 <= status_code < 400:
            self.__add_to_messenger(
                message=DefaultResponse300FailMessage.message,
                code=DefaultResponse300FailMessage.code,
                type_=DefaultResponse300FailMessage.type,
            )

        elif 400 <= status_code < 500:
            if status_code == 400:
                self.__add_to_messenger(
                    message=DefaultResponse400FailMessage.message,
                    code=DefaultResponse400FailMessage.code,
                    type_=DefaultResponse400FailMessage.type,
                )

            elif status_code == 401:
                self.__add_to_messenger(
                    message=DefaultResponse401FailMessage.message,
                    code=DefaultResponse401FailMessage.code,
                    type_=DefaultResponse401FailMessage.type,
                )

            elif status_code == 403:
                self.__add_to_messenger(
                    message=DefaultResponse403FailMessage.message,
                    code=DefaultResponse403FailMessage.code,
                    type_=DefaultResponse403FailMessage.type,
                )

            elif status_code == 404:
                self.__add_to_messenger(
                    message=DefaultResponse404FailMessage.message,
                    code=DefaultResponse404FailMessage.code,
                    type_=DefaultResponse404FailMessage.type,
                )

            elif status_code == 421:
                self.__add_to_messenger(
                    message=DefaultResponse421FailMessage.message,
                    code=DefaultResponse421FailMessage.code,
                    type_=DefaultResponse421FailMessage.type,
                )

            else:
                self.__add_to_messenger(
                    message=DefaultResponse400FailMessage.message,
                    code=DefaultResponse400FailMessage.code,
                    type_=DefaultResponse400FailMessage.type,
                )

        elif 500 <= status_code:
            self.__add_to_messenger(
                message=DefaultResponse500FailMessage.message,
                code=DefaultResponse500FailMessage.code,
                type_=DefaultResponse500FailMessage.type,
            )

        else:
            pass

    def __set_default_message(self):
        self.__default_messenger_message_adder()

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
                # if rslt:
                tmp.append(rslt)

            ret = tmp
            return ret

        if isinstance(data, dict):
            tmp = {}
            for k, v in data.items():
                rslt = self.__set_messages_from_data(v)
                # if rslt is not None:
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


class CreateAPIView(BaseAPI, DRFGCreateAPIView):
    def create(self, request, *args, **kwargs):
        if hasattr(self, 'check_validate_user') and self.check_validate_user:
            user_lookup_field = 'id'
            if hasattr(self, 'user_lookup_field'):
                user_lookup_field = self.user_lookup_field
            if not _valid_user(request=request, user_id=kwargs.get(user_lookup_field)):
                return Response(status=403)

        data = request.data.copy()
        user_field_name = 'user'
        if hasattr(self, 'user_field_name'):
            user_field_name = self.user_field_name
        data[user_field_name] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListAPIView(BaseAPI, DRFGListAPIView):
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self, 'for_user') and self.for_user:
            qs.filter(user_id=self.request.user.id)
        return qs

    def get(self, request, *args, **kwargs):
        if hasattr(self, 'check_validate_user') and self.check_validate_user:
            user_lookup_field = 'id'
            if hasattr(self, 'user_lookup_field'):
                user_lookup_field = self.user_lookup_field
            if not _valid_user(request=request, user_id=kwargs.get(user_lookup_field)):
                return Response(status=403)
        return super().get(request, *args, **kwargs)


class RetrieveAPIView(BaseAPI, DRFGRetrieveAPIView):
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self, 'for_user') and self.for_user:
            qs.filter(user_id=self.request.user.id)
        return qs

    def get(self, request, *args, **kwargs):
        if hasattr(self, 'check_validate_user') and self.check_validate_user:
            user_lookup_field = 'id'
            if hasattr(self, 'user_lookup_field'):
                user_lookup_field = self.user_lookup_field
            if not _valid_user(request=request, user_id=kwargs.get(user_lookup_field)):
                return Response(status=403)
        return super().get(request, *args, **kwargs)


class UpdateAPIView(BaseAPI, DRFGUpdateAPIView):
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self, 'for_user') and self.for_user:
            qs.filter(user_id=self.request.user.id)
        return qs

    def update(self, request, *args, **kwargs):
        if hasattr(self, 'check_validate_user') and self.check_validate_user:
            user_lookup_field = 'id'
            if hasattr(self, 'user_lookup_field'):
                user_lookup_field = self.user_lookup_field
            if not _valid_user(request=request, user_id=kwargs.get(user_lookup_field)):
                return Response(status=403)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data.copy()
        user_field_name = 'user'
        if hasattr(self, 'user_field_name'):
            user_field_name = self.user_field_name
        data[user_field_name] = request.user.id

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class DestroyAPIView(BaseAPI, DRFGDestroyAPIView):
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self, 'for_user') and self.for_user:
            qs.filter(user_id=self.request.user.id)
        return qs

    def delete(self, request, *args, **kwargs):
        if hasattr(self, 'check_validate_user') and self.check_validate_user:
            user_lookup_field = 'id'
            if hasattr(self, 'user_lookup_field'):
                user_lookup_field = self.user_lookup_field
            if not _valid_user(request=request, user_id=kwargs.get(user_lookup_field)):
                return Response(status=403)
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance=instance, soft_delete=kwargs.get('soft_delete', False))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance, soft_delete=False):
        if instance is None:
            return

        if soft_delete:
            instance.available = 0
            instance.save()
        else:
            instance.delete()
