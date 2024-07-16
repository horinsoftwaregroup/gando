from .base import DeveloperResponseAPIMessage
from .definitions import (
    DEVELOPER_WARNING,
    BASE_DEVELOPER_WARNING_STATUSCODE,
    BASE_DEVELOPER_WARNING_MESSAGE,
    BASE_DEVELOPER_WARNING_CODE,
)


class DeveloperWarningResponseAPIMessage(DeveloperResponseAPIMessage):
    def __init__(
        self,
        message=BASE_DEVELOPER_WARNING_MESSAGE,
        code=BASE_DEVELOPER_WARNING_CODE,
        typ=DEVELOPER_WARNING,
        status_code=BASE_DEVELOPER_WARNING_STATUSCODE
    ):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )
