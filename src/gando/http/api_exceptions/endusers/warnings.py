from .base import EnduserResponseAPIMessage
from .definitions import (
    ENDUSER_WARNING,
    BASE_ENDUSER_WARNING_STATUSCODE,
    BASE_ENDUSER_WARNING_MESSAGE,
    BASE_ENDUSER_WARNING_CODE,
)


class EnduserWarningResponseAPIMessage(EnduserResponseAPIMessage):
    def __init__(
        self,
        message=BASE_ENDUSER_WARNING_MESSAGE,
        code=BASE_ENDUSER_WARNING_CODE,
        typ=ENDUSER_WARNING,
        status_code=BASE_ENDUSER_WARNING_STATUSCODE
    ):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )
