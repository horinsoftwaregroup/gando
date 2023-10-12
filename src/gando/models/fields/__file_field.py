from django.db import models

from gando.utils.uploaders.files import FileUploadTo

from . import BaseMultiplyField


class File:
    def __init__(self, **kwargs):
        self.default_name = kwargs.get('default_name')
        self.src = kwargs.get('src')


class FileProperty:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if not instance:
            return self

        default_name = getattr(instance, self.name + '_default_name')
        src = getattr(instance, self.name + '_src')

        ret = File(default_name=default_name, src=src)
        return ret

    def __set__(self, instance, value):
        setattr(instance, self.name + '_default_name', value.name)
        setattr(instance, self.name + '_src', value)


class FileField(BaseMultiplyField):

    def contribute_to_class(self, cls, name, private_only=False):
        self.sub_field_contribute_to_class(
            cls,
            field_name=name,
            sub_field_name='default_name',
            sub_filed_class=models.TextField,
        )
        self.sub_field_contribute_to_class(
            cls,
            field_name=name,
            sub_field_name='src',
            sub_filed_class=models.FileField,
            sub_field_default_attr={
                'upload_to': FileUploadTo()
            }
        )
        setattr(cls, name, FileProperty(name))
