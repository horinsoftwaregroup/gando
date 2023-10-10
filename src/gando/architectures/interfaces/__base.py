from gando.http.responses.schemas import ResponseSchema
from gando.http.requests.schemas import RequestSchema
from gando.http.requests.methods import (
    GET,
    POST,
    PUT,
    PATCH,
    DELETE,
    HEAD,
    OPTIONS,
    TRACE,
)


class Base:
    http_method_names = [
        GET,
        POST,
        PUT,
        PATCH,
        DELETE,
        HEAD,
        OPTIONS,
        TRACE,
    ]

    def __init__(self, request: RequestSchema, **kwargs):
        self.request: RequestSchema = request
        for key, value in kwargs.items():
            setattr(self, key, value)

    def execute(self, *args, **kwargs):
        return self.dispatch(self.request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        response = ResponseSchema(
            success=False,
            status_code=405,
            messages={
                'info': [{'allowed_methods': self._allowed_methods()}],
                'error': [{'method': 'Method Not Allowed.'}],
            },
        )

        return response

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]


class BaseInterface(Base):
    pass
