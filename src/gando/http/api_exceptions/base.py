from rest_framework.exceptions import APIException


class ResponseAPIMessage(APIException):
    def __init__(self, message=None, code=None, typ=None, status_code=500):
        super().__init__(detail=message, code=code)
        self.typ = typ
        self.status_code = status_code
        self.code = code
        self.message = message
