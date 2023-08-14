from django.utils.deprecation import MiddlewareMixin
from gando.http.response import JsonResponse as Response


class JsonResponse(MiddlewareMixin):

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        rsp = Response(status=self.__get_status_code(response), **response.__dict__)
        return rsp

    def __get_status_code(self, response):
        try:
            status_code = getattr(response, 'status')
        except:
            status_code = getattr(response, 'status_code')
        return status_code
