from django.utils.translation import gettext_lazy as _
from django.db import models

from gando.utils.converters.images import small_blur_base64
from gando.utils.uploaders.images import ImageUploadTo


class BlurBase64Field(models.TextField):
    def formfield(self, **kwargs):
        return None

    def pre_save(self, model_instance, add):
        _src = getattr(model_instance, f'{self.PARENT_FIELD_NAME}_src')

        setattr(model_instance, self.attname, small_blur_base64(_src.file.name))
        return super().pre_save(model_instance, add)


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

        setattr(sub_field, 'PARENT_FIELD_NAME', field_name)

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


class Image:
    def __init__(self, **kwargs):
        self.alt = kwargs.get('alt')
        self.description = kwargs.get('description')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.src = kwargs.get('src')
        self.blur_base64 = kwargs.get('blur_base64')


class ImageProperty:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if not instance:
            return self

        ret = Image(
            alt=getattr(instance, self.name + '_alt'),
            description=getattr(instance, self.name + '_description'),
            width=getattr(instance, self.name + '_width'),
            height=getattr(instance, self.name + '_height'),
            src=getattr(instance, self.name + '_src'),
            blur_base64=getattr(instance, self.name + '_blur_base64'),
        )
        return ret

    def __set__(self, instance, value: dict):
        src = value.get('src')

        blur_base64 = small_blur_base64(src) if src.name.split('.')[-1] != 'svg' else None

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
            instance, self.name + '_blur_base64', blur_base64)


class ImageField(BaseMultiplyField):

    def contribute_to_class(self, cls, name, private_only=False):
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
            sub_field_name='blur_base64',
            sub_filed_class=BlurBase64Field,
            sub_field_default_attr={
                'verbose_name': _(f'{name[0].upper()}{name[1:].lower()} Blur-Base64'),
                'blank': True,
                'null': True,
            }
        )

        setattr(cls, name, ImageProperty(name))
