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

    @staticmethod
    def __data_parser(data: Optional[dict | list | str]) -> (dict, bool):
        if isinstance(data, str):
            ret = {'result': data}
            many = False
        elif isinstance(data, list):
            ret = {
                'count': len(data),
                'next': None,
                'previous': None,
                'results': data,
            }
            many = True
        elif isinstance(data, dict):
            if bool(data.get('results')):
                many = True
                ret = data
            else:
                many = False
                ret = {'result': data}
        else:
            ret = {'result': {}}
            many = False
        return ret, many
