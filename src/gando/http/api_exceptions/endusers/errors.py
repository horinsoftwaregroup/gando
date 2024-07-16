from .base import EnduserResponseAPIMessage
from .definitions import (
    ENDUSER_ERROR,
    BASE_ENDUSER_ERROR_STATUSCODE,
    BASE_ENDUSER_ERROR_MESSAGE,
    BASE_ENDUSER_ERROR_CODE,
)


class EnduserErrorResponseAPIMessage(EnduserResponseAPIMessage):
    def __init__(
        self,
        message=BASE_ENDUSER_ERROR_MESSAGE,
        code=BASE_ENDUSER_ERROR_CODE,
        typ=ENDUSER_ERROR,
        status_code=BASE_ENDUSER_ERROR_STATUSCODE
    ):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )


class EnduserErrorResponseAPIMessageBadRequest400(EnduserErrorResponseAPIMessage):
    def __init__(self, message=BASE_ENDUSER_ERROR_MESSAGE, code='bad_request'):
        super().__init__(
            message=message,
            code=code,
        )


class EnduserErrorResponseAPIMessageForbidden403(EnduserErrorResponseAPIMessage):
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


class EnduserErrorResponseAPIMessageUnauthorized401(EnduserErrorResponseAPIMessage):
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


class EnduserErrorResponseAPIMessageNotFound404(EnduserErrorResponseAPIMessage):
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
