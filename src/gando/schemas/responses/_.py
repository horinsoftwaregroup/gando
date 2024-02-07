from typing import List
from gando.schemas import AbstractBaseSchema


class Messenger(AbstractBaseSchema):
    type: str | None = None
    code: int | None = None
    message: str | None = None


class Data(AbstractBaseSchema):
    result: dict = dict()


class ListData(AbstractBaseSchema):
    count: int = 0
    next: str | None = None
    previous: str | None = None
    results: list = list()


class DevelopmentMessages(AbstractBaseSchema):
    info: list = list()
    warning: list = list()
    error: list = list()
    log: list = list()
    exception: list = list()


class BaseResponseSchema(AbstractBaseSchema):

    def __init__(self, response):
        response = response.json()

        success = response.get('success')
        status_code = response.get('status_code')
        has_warning = response.get('has_warning')
        exception_status = response.get('exception_status')
        monitor = response.get('monitor', {})
        messenger = response.get('messenger', [])
        many = response.get('many')
        data = response.get('data', {})
        development_messages = response.get('development_messages', {})
        kw = {
            'success': success,
            'status_code': status_code,
            'has_warning': has_warning,
            'exception_status': exception_status,
            'monitor': monitor,
            'messenger': messenger,
            'many': many,
            'data': ListData(**data) if many else Data(**data),
            'development_messages': development_messages,
        }

        super().__init__(**kw)

    success: bool = True
    status_code: int = 200
    has_warning: bool = False
    exception_status: bool = False
    monitor: dict = {}
    messenger: List[Messenger] = []
    many: bool = False
    data: Data | ListData = Data()
    development_messages: DevelopmentMessages = DevelopmentMessages()
