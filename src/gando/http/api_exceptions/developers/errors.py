from .base import DeveloperResponseAPIMessage
from .definitions import (
    DEVELOPER_ERROR,
    BASE_DEVELOPER_ERROR_STATUSCODE,
    BASE_DEVELOPER_ERROR_MESSAGE,
    BASE_DEVELOPER_ERROR_CODE,
)


class DeveloperErrorResponseAPIMessage(DeveloperResponseAPIMessage):
    def __init__(
        self,
        message=BASE_DEVELOPER_ERROR_MESSAGE,
        code=BASE_DEVELOPER_ERROR_CODE,
        typ=DEVELOPER_ERROR,
        status_code=BASE_DEVELOPER_ERROR_STATUSCODE
    ):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )


class DeveloperErrorResponseAPIMessageBadRequest400(DeveloperErrorResponseAPIMessage):
    def __init__(self, message=BASE_DEVELOPER_ERROR_MESSAGE, code='bad_request'):
        super().__init__(
            message=message,
            code=code,
        )


class DeveloperErrorResponseAPIMessageForbidden403(DeveloperErrorResponseAPIMessage):
    def __init__(
        self,
        message="You do not have permission to access this resource. "
                "Please do not try again, "
                "or if you doubt the authenticity of the requested permissions, "
                "try again after checking the authenticity of the permissions.",
        code='forbidden',
    ):
        super().__init__(
            message=message,
            code=code,
            status_code=403,
        )


class DeveloperErrorResponseAPIMessageUnauthorized401(DeveloperErrorResponseAPIMessage):
    def __init__(
        self,
        message="To access this tool, you need to submit authentication documents. "
                "However, the documents required for authentication are not available or "
                "the documents have expired. "
                "Please check the desired documents and repeat the request again.",
        code='unauthorized',
    ):
        super().__init__(
            message=message,
            code=code,
            status_code=401,
        )


class DeveloperErrorResponseAPIMessageNotFound404(DeveloperErrorResponseAPIMessage):
    def __init__(
        self,
        message="The data you are looking for was not found.",
        code='not_found',
    ):
        super().__init__(
            message=message,
            code=code,
            status_code=404,
        )
