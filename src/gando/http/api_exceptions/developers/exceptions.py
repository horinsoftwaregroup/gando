from .base import DeveloperResponseAPIMessage
from .definitions import (
    DEVELOPER_EXCEPTION,
    BASE_DEVELOPER_EXCEPTION_STATUSCODE,
    BASE_DEVELOPER_EXCEPTION_MESSAGE,
    BASE_DEVELOPER_EXCEPTION_CODE,
)


class DeveloperExceptionResponseAPIMessage(DeveloperResponseAPIMessage):
    def __init__(
        self,
        message=BASE_DEVELOPER_EXCEPTION_MESSAGE,
        code=BASE_DEVELOPER_EXCEPTION_CODE,
        typ=DEVELOPER_EXCEPTION,
        status_code=BASE_DEVELOPER_EXCEPTION_STATUSCODE
    ):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )


class DeveloperExceptionResponseAPIMessageInternalServerError500(DeveloperExceptionResponseAPIMessage):
    def __init__(self, message=BASE_DEVELOPER_EXCEPTION_MESSAGE, code='internal_server_error'):
        super().__init__(
            message=message,
            code=code,
        )
