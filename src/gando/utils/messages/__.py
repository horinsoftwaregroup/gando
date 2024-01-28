class BaseMessage:
    def __init__(self, message, code, type_, *args, **kwargs):
        self.message = message
        self.code = code
        self.type = type_


class BaseFailMessage(BaseMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(type_='FAIL', *args, **kwargs)


class BaseWarningMessage(BaseMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(type_='WARNING', *args, **kwargs)


class BaseSuccessMessage(BaseMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(type_='SUCCESS', *args, **kwargs)


class BaseInfoMessage(BaseMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(type_='INFO', *args, **kwargs)


class _DefaultResponse100FailMessage(BaseFailMessage):
    def __init__(self):
        super().__init__(
            message='please wait...',
            code='100',
        )


DefaultResponse100FailMessage = _DefaultResponse100FailMessage()


class _DefaultResponse200SuccessMessage(BaseSuccessMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message='Your request has been successfully registered.',
            code='200',
        )


DefaultResponse200SuccessMessage = _DefaultResponse200SuccessMessage()


class _DefaultResponse201SuccessMessage(BaseSuccessMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message='The desired object was created correctly.',
            code='201',
        )


DefaultResponse201SuccessMessage = _DefaultResponse201SuccessMessage()


class _DefaultResponse300FailMessage(BaseFailMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message='The requirements for your request are not available.',
            code='300',
        )


DefaultResponse300FailMessage = _DefaultResponse300FailMessage()


class _DefaultResponse400FailMessage(BaseFailMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message='Bad Request...',
            code='400',
        )


DefaultResponse400FailMessage = _DefaultResponse400FailMessage()


class _DefaultResponse401FailMessage(BaseFailMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message='Your authentication information is not available.',
            code='401',
        )


DefaultResponse401FailMessage = _DefaultResponse401FailMessage()


class _DefaultResponse403FailMessage(BaseFailMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message='You do not have access to this section.',
            code='403',
        )


DefaultResponse403FailMessage = _DefaultResponse403FailMessage()


class _DefaultResponse404FailMessage(BaseFailMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message='There is no information about your request.',
            code='404',
        )


DefaultResponse404FailMessage = _DefaultResponse404FailMessage()


class _DefaultResponse421FailMessage(BaseFailMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message=(
                "An unexpected error has occurred based on your request type.\n"
                "Please do not repeat this request without changing your request.\n"
                "Be sure to read the documents on how to use this service correctly.\n"
                "In any case, discuss the issue with support.\n"
            ),
            code='421',
        )


DefaultResponse421FailMessage = _DefaultResponse421FailMessage()


class _DefaultResponse500FailMessage(BaseFailMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message='The server is unable to respond to your request.',
            code='500',
        )


DefaultResponse500FailMessage = _DefaultResponse500FailMessage()
