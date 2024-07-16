from gando.http.api_exceptions.base import ResponseAPIMessage


class EnduserResponseAPIMessage(ResponseAPIMessage):
    def __init__(self, message=None, code=None, typ=None, status_code=None):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )
