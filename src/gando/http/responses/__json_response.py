from typing import Optional, List, Dict

from django.http.response import JsonResponse as DJJsonResponse

from gando.config import SETTINGS

from .schemas import ResponseSchema


class JsonResponse(DJJsonResponse):
    def __init__(
        self,

        data: Optional[dict | list | str] = None,

        log_messages__: Optional[List[Dict[str, str]]] = None,
        info_messages__: Optional[List[Dict[str, str]]] = None,
        warning_messages__: Optional[List[Dict[str, str]]] = None,
        error_messages__: Optional[List[Dict[str, str]]] = None,
        exception_messages__: Optional[List[Dict[str, str]]] = None,

        monitor__: dict = None,

        **kwargs,
    ):
        data, many, monitor, msgs = self.__data_parser(
            data,
            monitor__=monitor__,
            log_messages__=log_messages__,
            info_messages__=info_messages__,
            warning_messages__=warning_messages__,
            error_messages__=error_messages__,
            exception_messages__=exception_messages__,
        )

        context = {
            'success': not (bool(msgs['error_messages']) or bool(msgs['exception_messages'])),
            'has_warning': bool(msgs['warning_messages']),
            'monitor': monitor,
            'messages': {
                'log': msgs['log_messages'] or [] if SETTINGS.DEBUG else [],
                'info': msgs['info_messages'] or [],
                'warning': msgs['warning_messages'] or [],
                'error': msgs['error_messages'] or [],
                'exception': msgs['exception_messages'] or [],
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

    def __data_parser(self, data: Optional[dict | list | str], **kwargs):

        monitor = kwargs.get('monitor__') or {}
        many = False
        msgs = {
            'log_messages': kwargs.get('log_messages__') or [],
            'info_messages': kwargs.get('info_messages__') or [],
            'warning_messages': kwargs.get('warning_messages__') or [],
            'error_messages': kwargs.get('error_messages__') or [],
            'exception_messages': kwargs.get('exception_messages__') or [],
        }
        msgs__ = {}

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
            data, mntr = self.__monitor_detector(data)
            mntr.update(monitor)
            monitor = mntr

            data, msgs__ = self.__messages_detector(data)
            if bool(data.get('results')):
                many = True
                data_response = data

            else:
                data_response = {'result': data}

        else:
            data_response = {'result': {}}

        msgs['log_messages'] += msgs__.get('log_messages', [])
        msgs['info_messages'] += msgs__.get('info_messages', [])
        msgs['warning_messages'] += msgs__.get('warning_messages', [])
        msgs['error_messages'] += msgs__.get('error_messages', [])
        msgs['exception_messages'] += msgs__.get('exception_messages', [])

        ret = data_response, many, monitor, msgs
        return ret

    def __monitor_detector(self, data):
        monitor = {}
        for i in SETTINGS.MONITOR_KEYS:
            mntr = data.pop(i, None)
            if mntr is not None:
                monitor[i] = mntr
        return data, monitor

    def __messages_detector(self, data: dict) -> (dict, dict):
        msg = {
            'log_messages': data.pop('log_messages', []),
            'info_messages': data.pop('info_messages', []),
            'warning_messages': data.pop('warning_messages', []),
            'error_messages': data.pop('error_messages', []),
            'exception_messages': data.pop('exception_messages', []),
        }
        return data, msg
