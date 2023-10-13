from django_resized import ResizedImageField

from django.utils.translation import gettext_lazy as _
from django.db import models

from gando.utils.converters.images import small_blur_base64
from gando.utils.uploaders.images import ImageUploadTo
from gando.utils.uploaders.files import FileUploadTo


class BaseMultiplyField(models.Field):
    def __init__(self, **kwargs):
        self.field_kwargs = kwargs

        super().__init__(**{})

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
            sub_field_default_attr={
                'verbose_name': _(f'{name[0].upper()}{name[1:].lower()} Default Name'),
                'blank': True,
                'null': True,
            }
        )
        self.sub_field_contribute_to_class(
            cls,
            field_name=name,
            sub_field_name='src',
            sub_filed_class=models.FileField,
            sub_field_default_attr={
                'verbose_name': _(f'{name[0].upper()}{name[1:].lower()} SRC'),
                'upload_to': FileUploadTo(),
                'blank': True,
                'null': True,
            }
        )
        setattr(cls, name, FileProperty(name))


class Image:
    def __init__(self, **kwargs):
        self.default_name = kwargs.get('default_name')

        self.alt = kwargs.get('alt')
        self.description = kwargs.get('description')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.src = kwargs.get('src')
        self.customize_src = kwargs.get('customize_src')
        self.blur_base64 = kwargs.get('blur_base64')


class ImageProperty:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if not instance:
            return self

        ret = Image(
            default_name=getattr(instance, self.name + '_default_name'),
            alt=getattr(instance, self.name + '_alt'),
            description=getattr(instance, self.name + '_description'),
            width=getattr(instance, self.name + '_width'),
            height=getattr(instance, self.name + '_height'),
            src=getattr(instance, self.name + '_src'),
            customize_src=getattr(instance, self.name + '_customize_src'),
            blur_base64=getattr(instance, self.name + '_blur_base64'),
        )
        return ret

    def __set__(self, instance, value: dict):
        src = value.get('src')
        if src:
            if src.name.split('.')[-1] == 'svg':
                customize_src = None
                blur_base64 = None
            else:
                customize_src = src.file
                blur_base64 = small_blur_base64(src)

            setattr(
                instance, self.name + '_default_name', src.name)
            setattr(
                instance, self.name + '_alt', value.get('alt'))
            setattr(
                instance, self.name + '_description', value.get('description'))
            setattr(
                instance, self.name + '_width', value.get('width'))
            setattr(
                instance, self.name + '_height', value.get('height'))
            setattr(
                instance, self.name + '_src', src)
            setattr(
                instance, self.name + '_customize_src', customize_src)
            setattr(
                instance, self.name + '_blur_base64', blur_base64)


class ImageField(BaseMultiplyField):

    def contribute_to_class(self, cls, name, private_only=False):
        self.sub_field_contribute_to_class(
            cls,
            field_name=name,
            sub_field_name='default_name',
            sub_filed_class=models.TextField,
            sub_field_default_attr={
                'verbose_name': _(f'{name[0].upper()}{name[1:].lower()} Default Name'),
                'blank': True,
                'null': True,
            }
        )
        self.sub_field_contribute_to_class(
            cls,
            field_name=name,
            sub_field_name='alt',
            sub_filed_class=models.CharField,
            sub_field_default_attr={
                'verbose_name': _(f'{name[0].upper()}{name[1:].lower()} Alternate Title'),
                'help_text': _('This title will be shown instead if the image is not loaded.'),
                'max_length': 255,
                'blank': True,
                'null': True,
            }
        )
        self.sub_field_contribute_to_class(
            cls,
            field_name=name,
            sub_field_name='description',
            sub_filed_class=models.TextField,
            sub_field_default_attr={
                'verbose_name': _(f'{name[0].upper()}{name[1:].lower()} Description'),
                'help_text': _("If you want a text to be written below the image,"
                               " write it here. Otherwise, leave it blank."),
                'blank': True,
                'null': True,
            }
        )
        self.sub_field_contribute_to_class(
            cls,
            field_name=name,
            sub_field_name='width',
            sub_filed_class=models.PositiveIntegerField,
            sub_field_default_attr={
                'verbose_name': _(f'{name[0].upper()}{name[1:].lower()} Width'),
                'blank': True,
                'null': True,
            }
        )
        self.sub_field_contribute_to_class(
            cls,
            field_name=name,
            sub_field_name='height',
            sub_filed_class=models.PositiveIntegerField,
            sub_field_default_attr={
                'verbose_name': _(f'{name[0].upper()}{name[1:].lower()} Height'),
                'blank': True,
                'null': True,
            }
        )
        self.sub_field_contribute_to_class(
            cls,
            field_name=name,
            sub_field_name='src',
            sub_filed_class=models.ImageField,
            sub_field_default_attr={
                'verbose_name': _(f'{name[0].upper()}{name[1:].lower()} SRC'),
                'upload_to': ImageUploadTo(),
                'blank': True,
                'null': True,

                'width_field': f'{name}_width',
                'height_field': f'{name}_height',
            }
        )
        self.sub_field_contribute_to_class(
            cls,
            field_name=name,
            sub_field_name='customize_src',
            sub_filed_class=ResizedImageField,
            sub_field_default_attr={
                'verbose_name': _(f'{name[0].upper()}{name[1:].lower()} Customized SRC'),
                'upload_to': ImageUploadTo(),
                'blank': True,
                'null': True,

                'width_field': f'{name}_width',
                'height_field': f'{name}_height',

                'size': [100, 100],
                'scale': 0.5,
                'crop': None,
                'quality': 75,
                'keep_meta': True,
                'force_format': 'PNG',
            }
        )
        self.sub_field_contribute_to_class(
            cls,
            field_name=name,
            sub_field_name='blur_base64',
            sub_filed_class=models.TextField,
            sub_field_default_attr={
                'verbose_name': _(f'{name[0].upper()}{name[1:].lower()} Blur-Base64'),
                'blank': True,
                'null': True,
            }
        )

        setattr(cls, name, ImageProperty(name))
