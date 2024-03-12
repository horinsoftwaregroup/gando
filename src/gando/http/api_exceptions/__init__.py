from rest_framework.exceptions import APIException

DEVELOPER_EXCEPTION = 'developer_exception'
DEVELOPER_ERROR = 'developer_error'
DEVELOPER_WARNING = 'developer_warning'
ENDUSER_FAIL = 'enduser_fail'
ENDUSER_ERROR = 'enduser_error'
ENDUSER_WARNING = 'enduser_warning'


class ResponseAPIMessage(APIException):
    def __init__(self, message=None, code=None, typ=None, status_code=500):
        super().__init__(detail=message, code=code)
        self.typ = typ
        self.status_code = status_code
        self.code = code
        self.message = message


class DeveloperResponseAPIMessage(ResponseAPIMessage):
    def __init__(self, message=None, code=None, typ=None, status_code=None):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )


class DeveloperExceptionResponseAPIMessage(DeveloperResponseAPIMessage):
    def __init__(self, message=None, code=None, typ=None, status_code=None):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )


class DeveloperErrorResponseAPIMessage(DeveloperResponseAPIMessage):
    def __init__(self, message=None, code=None, typ=None, status_code=None):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )


class DeveloperWarningResponseAPIMessage(DeveloperResponseAPIMessage):
    def __init__(self, message=None, code=None, typ=None, status_code=None):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )


class DeveloperExceptionResponseAPIMessageBadRequest(DeveloperExceptionResponseAPIMessage):
    def __init__(self, message='Bad Request', code='bad_request'):
        super().__init__(
            message=message,
            code=code,
            typ=DEVELOPER_EXCEPTION,
            status_code=400,
        )


class DeveloperErrorResponseAPIMessageBadRequest(DeveloperErrorResponseAPIMessage):
    def __init__(self, message='Bad Request', code='bad_request'):
        super().__init__(
            message=message,
            code=code,
            typ=DEVELOPER_ERROR,
            status_code=400,
        )


class DeveloperWarningResponseAPIMessageBadRequest(DeveloperWarningResponseAPIMessage):
    def __init__(self, message='Bad Request', code='bad_request'):
        super().__init__(
            message=message,
            code=code,
            typ=DEVELOPER_WARNING,
            status_code=400,
        )


class DeveloperExceptionResponseAPIMessageForbidden403(DeveloperExceptionResponseAPIMessage):
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
            typ=DEVELOPER_EXCEPTION,
            status_code=403,
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
            typ=DEVELOPER_ERROR,
            status_code=403,
        )


class DeveloperWarningResponseAPIMessageForbidden403(DeveloperWarningResponseAPIMessage):
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
            typ=DEVELOPER_WARNING,
            status_code=403,
        )


class EnduserResponseAPIMessage(ResponseAPIMessage):
    def __init__(self, message=None, code=None, typ=None, status_code=None):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )


class EnduserFailResponseAPIMessage(EnduserResponseAPIMessage):
    def __init__(self, message=None, code=None, typ=None, status_code=None):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )


class EnduserErrorResponseAPIMessage(EnduserResponseAPIMessage):
    def __init__(self, message=None, code=None, typ=None, status_code=None):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )


class EnduserWarningResponseAPIMessage(EnduserResponseAPIMessage):
    def __init__(self, message=None, code=None, typ=None, status_code=None):
        super().__init__(
            message=message,
            code=code,
            typ=typ,
            status_code=status_code,
        )


class EnduserFailResponseAPIMessageBadRequest(EnduserFailResponseAPIMessage):
    def __init__(self, message='Bad Request', code='bad_request'):
        super().__init__(
            message=message,
            code=code,
            typ=ENDUSER_FAIL,
            status_code=400,
        )


class EnduserErrorResponseAPIMessageBadRequest(EnduserErrorResponseAPIMessage):
    def __init__(self, message='Bad Request', code='bad_request'):
        super().__init__(
            message=message,
            code=code,
            typ=ENDUSER_ERROR,
            status_code=400,
        )


class EnduserWarningResponseAPIMessageBadRequest(EnduserWarningResponseAPIMessage):
    def __init__(self, message='Bad Request', code='bad_request'):
        super().__init__(
            message=message,
            code=code,
            typ=ENDUSER_WARNING,
            status_code=400,
        )


class EnduserFailResponseAPIMessageForbidden403(EnduserFailResponseAPIMessage):
    def __init__(
        self,
        message='You do not have permission to access this resource. Please do not try again.',
        code='forbidden',
    ):
        super().__init__(
            message=message,
            code=code,
            typ=ENDUSER_FAIL,
            status_code=403,
        )


class EnduserErrorResponseAPIMessageForbidden403(EnduserErrorResponseAPIMessage):
    def __init__(
        self,
        message='You do not have permission to access this resource. Please do not try again.',
        code='forbidden',
    ):
        super().__init__(
            message=message,
            code=code,
            typ=ENDUSER_ERROR,
            status_code=403,
        )


class EnduserWarningResponseAPIMessageForbidden403(EnduserWarningResponseAPIMessage):
    def __init__(
        self,
        message='You do not have permission to access this resource. Please do not try again.',
        code='forbidden',
    ):
        super().__init__(
            message=message,
            code=code,
            typ=ENDUSER_WARNING,
            status_code=403,
        )
