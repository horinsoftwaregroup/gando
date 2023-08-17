from typing import Optional, List, Dict

from django.http.response import JsonResponse as DJJsonResponse
from django.conf import settings

from .schemas import ResponseSchema

debug_status = settings.DEBUG


class JsonResponse(DJJsonResponse):
    def __init__(
        self,

        data: Optional[dict | list | str] = None,

        log_messages: Optional[List[Dict[str, str]]] = None,
        info_messages: Optional[List[Dict[str, str]]] = None,
        warning_messages: Optional[List[Dict[str, str]]] = None,
        error_messages: Optional[List[Dict[str, str]]] = None,
        exception_messages: Optional[List[Dict[str, str]]] = None,

        **kwargs,
    ):
        data, many = self.__data_parser(data)

        context = {
            'success': not (bool(error_messages) and bool(exception_messages)),
            'has_warning': bool(warning_messages),
            'monitor': {},
            'messages': {
                'log': log_messages or [] if debug_status else [],
                'info': info_messages or [],
                'warning': warning_messages or [],
                'error': error_messages or [],
                'exception': exception_messages or [],
            },
            'data': data,
            'many': many,
        }
        context = context or {}
        data = ResponseSchema(**context).model_dump()
        super(JsonResponse, self).__init__(
            data,
            status=kwargs.get('status', 200)
        )

    def __data_parser(self, data: Optional[dict | list | str]) -> (dict, bool):
        monitor = {}
        many = False

        if isinstance(data, str):
            data_response = {'result': data}

        elif isinstance(data, list):
            data_response = {
                'count': len(data),
                'next': None,
                'previous': None,
                'results': data,
            }
            many = True

        elif isinstance(data, dict):
            data, monitor = self.___monitor_detector(data)
            if bool(data.get('results')):
                many = True
                data_response = data

            else:
                data_response = {'result': data}

        else:
            data_response = {'result': {}}

        ret = data_response, many, monitor
        return ret

    @property
    def __get_monitor_keys(self):
        return settings.MONITOR_KEYS or []

    def ___monitor_detector(self, data):
        monitor = {}
        for i in self.__get_monitor_keys:
            monitor[i] = data.pop(i, None)
        return data, monitor
