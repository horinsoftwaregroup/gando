class Helper:
    def __init__(
        self,
        allowed_methods: list = None,
        request_fields: dict = None,
        query_params: dict = None,
        expected_response_data_fields: dict = None
    ):
        self.allowed_methods = allowed_methods or []
        self.request_fields = request_fields or {}
        self.query_params = query_params or {}
        self.expected_response_data_fields = expected_response_data_fields or {}

    _allowed_methods = None

    @property
    def allowed_methods(self):
        return {
            'key': 'allowed_methods',
            'value': self._allowed_methods,
        }

    @allowed_methods.setter
    def allowed_methods(self, value):
        self._allowed_methods = value

    _request_fields = None

    @property
    def request_fields(self):
        return {
            'key': 'request_fields',
            'value': self._request_fields,
        }

    @request_fields.setter
    def request_fields(self, value):
        self._request_fields = value

    _query_params = None

    @property
    def query_params(self):
        return {
            'key': 'query_params',
            'value': self._query_params,
        }

    @query_params.setter
    def query_params(self, value):
        self._query_params = value

    _expected_response_data_fields = None

    @property
    def expected_response_data_fields(self):
        return {
            'key': 'expected_response_data_fields',
            'value': self._expected_response_data_fields,
        }

    @expected_response_data_fields.setter
    def expected_response_data_fields(self, value):
        self._expected_response_data_fields = value


class BaseField:
    STRING = 'String'
    CHARACTER = 'Character'
    TEXT = 'Text'
    INTEGER = 'Integer'
    FLOAT = 'Float'
    POSITIVE_INTEGER = 'PositiveInteger'
    NEGATIVE_INTEGER = 'NegativeInteger'
    POSITIVE_FLOAT = 'PositiveFloat'
    NEGATIVE_FLOAT = 'NegativeFloat'
    DATE = 'Date'
    DATETIME = 'DateTime'
    TIME = 'Time'
    FILE = 'File'
    IMAGE = 'Image'
    ID = 'ID'
    UUID = 'UUID'
    LIST = 'List'
    DICTIONARY = 'Dictionary'
    BOOLEAN = 'Boolean'

    OPTIONAL = 'Optional'
    REQUIRED = 'Required'

    UNKNOWN = 'Unknown'

    def __init__(self, **kwargs):
        self.typ = kwargs.get('typ', self.UNKNOWN)

        self.presentment = kwargs.get('presentment', self.OPTIONAL)

        self.min_length = kwargs.get('min_length')
        self.max_length = kwargs.get('max_length')

        self.min = kwargs.get('min')
        self.max = kwargs.get('max')

        self.error_message = kwargs.get('error_message')
        self.validator_pattern = kwargs.get('validator_pattern')

        self.description = kwargs.get('description')
        self.allowed_file_format = kwargs.get('allowed_file_format')
        self.allowed_image_format = kwargs.get('allowed_image_format')

    def todict(self):
        ret = {}
        if self.typ:
            ret['type'] = self.typ
        if self.presentment:
            ret['presentment'] = self.presentment
        if self.min_length:
            ret['min_length'] = self.min_length
        if self.max_length:
            ret['max_length'] = self.max_length
        if self.min:
            ret['min'] = self.min
        if self.max:
            ret['max'] = self.max
        if self.error_message:
            ret['error_message'] = self.error_message
        if self.validator_pattern:
            ret['validator_pattern'] = self.validator_pattern
        if self.description:
            ret['description'] = self.description
        if self.allowed_file_format:
            ret['allowed_file_format'] = self.allowed_file_format
        if self.allowed_image_format:
            ret['allowed_image_format'] = self.allowed_image_format

        return ret


class StringField(BaseField):
    def __init__(self, **kwargs):
        kwargs['typ'] = self.STRING
        super().__init__(**kwargs)


class UsernameField(StringField):
    def __init__(self, **kwargs):
        kwargs['min_length'] = 3
        kwargs['max_length'] = 31
        super().__init__(**kwargs)


class PasswordField(StringField):
    def __init__(self, **kwargs):
        kwargs['min_length'] = 8
        kwargs['max_length'] = 31
        super().__init__(**kwargs)


class EmailField(StringField):
    def __init__(self, **kwargs):
        kwargs['min_length'] = 8
        kwargs['max_length'] = 31
        super().__init__(**kwargs)


class DateField(BaseField):
    def __init__(self, **kwargs):
        kwargs['typ'] = self.DATE
        super().__init__(**kwargs)


class TimeField(BaseField):
    def __init__(self, **kwargs):
        kwargs['typ'] = self.TIME
        super().__init__(**kwargs)


class DateTimeField(BaseField):
    def __init__(self, **kwargs):
        kwargs['typ'] = self.DATETIME
        super().__init__(**kwargs)


class IntegerField(BaseField):
    def __init__(self, **kwargs):
        kwargs['typ'] = self.INTEGER
        super().__init__(**kwargs)


class FloatField(BaseField):
    def __init__(self, **kwargs):
        kwargs['typ'] = self.FLOAT
        super().__init__(**kwargs)


class FileField(BaseField):
    def __init__(self, **kwargs):
        kwargs['typ'] = self.FILE
        super().__init__(**kwargs)


class ImageField(BaseField):
    def __init__(self, **kwargs):
        kwargs['typ'] = self.IMAGE
        super().__init__(**kwargs)


class UUIDField(BaseField):
    def __init__(self, **kwargs):
        kwargs['typ'] = self.UUID
        super().__init__(**kwargs)


class IDField(BaseField):
    def __init__(self, **kwargs):
        kwargs['typ'] = self.ID
        super().__init__(**kwargs)


class ListField(BaseField):
    def __init__(self, **kwargs):
        kwargs['typ'] = self.LIST
        super().__init__(**kwargs)


class DictionaryField(BaseField):
    def __init__(self, **kwargs):
        kwargs['typ'] = self.DICTIONARY
        super().__init__(**kwargs)
