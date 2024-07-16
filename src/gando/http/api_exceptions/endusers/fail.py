from .base import EnduserResponseAPIMessage
from .definitions import (
    ENDUSER_FAIL,
    BASE_ENDUSER_FAIL_STATUSCODE,
    BASE_ENDUSER_FAIL_MESSAGE,
    BASE_ENDUSER_FAIL_CODE,
)


class EnduserFailResponseAPIMessage(EnduserResponseAPIMessage):
    def __init__(
        self,
        message=BASE_ENDUSER_FAIL_MESSAGE,
        code=BASE_ENDUSER_FAIL_CODE,
        typ=ENDUSER_FAIL,
        status_code=BASE_ENDUSER_FAIL_STATUSCODE
    ):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )


class EnduserFailResponseAPIMessageInternalServerError500(EnduserFailResponseAPIMessage):
    def __init__(self, message=BASE_ENDUSER_FAIL_MESSAGE, code=BASE_ENDUSER_FAIL_CODE):
        super().__init__(
            message=message,
            code=code,
        )
