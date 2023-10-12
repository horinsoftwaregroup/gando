from django.db import models


class BaseMultiplyField(models.Field):
    def __init__(self, **kwargs):
        self.field_kwargs = kwargs.pop('field_kwargs', {})
        super().__init__(**kwargs)

    def sub_field_contribute_to_class(
        self,

        cls,
        field_name,

        sub_field_name,
        sub_filed_class,
        sub_field_default_attr=None,
    ):

        my_kwargs = self.__get_my_kwargs(
            my_name=sub_field_name,
            kwargs=self.field_kwargs,
            default=sub_field_default_attr,
        )

        sub_field = sub_filed_class(
            name=field_name + f'_{sub_field_name}',
            **my_kwargs,
        )

        sub_field.contribute_to_class(cls, sub_field.name)

    @staticmethod
    def __get_my_kwargs(my_name, kwargs: dict, default: dict = None):
        kwargs_ = {}
        for k, v in kwargs.items():
            if f'{my_name}__' in k:
                kwargs_[k[len(f'{my_name}__'):]] = v

        default_ = default or {}
        for k, v in default_.items():
            if k not in kwargs_:
                kwargs_[k] = v

        return kwargs_
