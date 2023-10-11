from abc import abstractmethod
from pydantic import BaseModel

from django.db.models import Model

from gando.architectures.services import BaseService

FIRST_KEYWORD = 'first'
LAST_KEYWORD = 'last'
MANY_KEYWORD = 'many'
OBJECT_TYPE_KEYWORD = 'is_object'


class BaseGetterService(BaseService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.values = self.__values(*args)
        self.filters = self.__filters(**kwargs)

        self.many = self.__many(**kwargs)
        self.first_or_last = self.__first_or_last(*args, **kwargs)

        self.is_object = self.__is_object(**kwargs)

    @property
    @abstractmethod
    def model(self) -> Model:
        pass

    @property
    @abstractmethod
    def output_schema(self) -> BaseModel:
        pass

    @property
    @abstractmethod
    def filter_schema(self) -> BaseModel:
        pass

    @property
    @abstractmethod
    def acceptable_values(self) -> list:
        pass

    def service_output_handler(self, *args, **kwargs):
        ret = self.__get_from_db()
        return ret

    def convert_to_schema(self, obj):
        ret = self.output_schema(**obj) if obj else None
        return ret

    def convert_to_schema_many_true(self, objs):
        ret = [self.convert_to_schema(i) for i in objs]
        return ret

    def get_from_db(self):
        rslt = self.__query()

        if not self.is_object:
            if self.many:
                rslt = self.convert_to_schema_many_true(self.__query())
            else:
                rslt = self.convert_to_schema(self.__query())

        ret = rslt
        return ret

    def __values(self, *values) -> list:
        if values:
            tmp = set()
            for i in values:
                if i in self.acceptable_values:
                    tmp.add(i)

            values = list(tmp)

        ret = values if values else self.acceptable_values
        return ret

    def __filters(self, **filters) -> dict:
        inst = self.filter_schema(**filters)
        ret = inst.model_dump().extract()
        return ret

    def __many(self, *args, **kwargs) -> bool:
        many = kwargs.get(MANY_KEYWORD)
        if many is True or MANY_KEYWORD in args:
            return True

        return False

    def __first_or_last(self, *args, **kwargs) -> str:
        first = kwargs.get(FIRST_KEYWORD)
        if first is True or FIRST_KEYWORD in args:
            return FIRST_KEYWORD

        return LAST_KEYWORD

    def __is_object(self, **kwargs) -> bool:
        is_object = kwargs.get(OBJECT_TYPE_KEYWORD)
        if is_object is True:
            return True

        return False

    def __query_set(self):
        if self.is_object:
            qs = self.model.objects.filter(**self.filters)
        else:
            qs = self.model.objects.values(*self.values).filter(**self.filters)

        ret = qs
        return ret

    def __query(self):
        if self.many:
            q = self.__query_set().all()

        elif self.first_or_last == LAST_KEYWORD:
            q = self.__query_set().last()

        else:
            q = self.__query_set().first()

        ret = q
        return ret
