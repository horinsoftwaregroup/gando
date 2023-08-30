from django.core.management.base import BaseCommand, CommandError
import os
from gando.utils.strings.converters import casing
from gando.utils.strings.casings import PASCAL_CASE, CAMEL_CASE, KEBAB_CASE


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        """
        """
        parser.add_argument('-al', '--applabel', type=str, help='')
        parser.add_argument('-mn', '--modelname', type=str, help='')

    def handle(self, *args, **kwargs):
        self.app_label = kwargs
        self.model_name = kwargs

        self.model_name_is_valid(rais_exception=True)

        self.initial_model()
        self.initial_admin()
        self.initial_serializers()
        self.initial_views()
        self.initial_urlpatterns()

    # ....
    @property
    def base_path(self) -> str | None:
        from django.conf import settings

        ret = os.path.join(settings.BASE_DIR, self.app_label)
        return ret

    @property
    def repo_path(self) -> str | None:
        ret = os.path.join(self.base_path, 'repo')
        try:
            os.mkdir(ret)
        except:
            pass
        with open(os.path.join(ret, '__init__.py'), 'a') as f:
            pass
        return ret

    @property
    def models_path(self) -> str | None:
        ret = os.path.join(self.repo_path, 'models')
        try:
            os.mkdir(ret)
        except:
            pass
        with open(os.path.join(ret, '__init__.py'), 'a') as f:
            pass
        return ret

    @property
    def base_models_file(self) -> str | None:
        ret = os.path.join(self.base_path, 'models.py')
        with open(ret, 'a') as f:
            pass
        return ret

    @property
    def admin_path(self) -> str | None:
        ret = os.path.join(self.repo_path, 'admin')
        try:
            os.mkdir(ret)
        except:
            pass
        with open(os.path.join(ret, '__init__.py'), 'a') as f:
            pass
        return ret

    @property
    def base_admin_file(self) -> str | None:
        ret = os.path.join(self.base_path, 'admin.py')
        with open(ret, 'a') as f:
            pass
        return ret

    @property
    def serializers_path(self) -> str | None:
        ret = os.path.join(self.repo_path, 'serializers')
        try:
            os.mkdir(ret)
        except:
            pass
        with open(os.path.join(ret, '__init__.py'), 'a') as f:
            pass
        return ret

    @property
    def base_serializers_file(self) -> str | None:
        ret = os.path.join(self.base_path, 'serializers.py')
        with open(ret, 'a') as f:
            pass
        return ret

    @property
    def views_path(self) -> str | None:
        ret = os.path.join(self.repo_path, 'views')
        try:
            os.mkdir(ret)
        except:
            pass
        with open(os.path.join(ret, '__init__.py'), 'a') as f:
            pass
        return ret

    @property
    def base_views_file(self) -> str | None:
        ret = os.path.join(self.base_path, 'views.py')
        with open(ret, 'a') as f:
            pass
        return ret

    @property
    def urls_path(self) -> str | None:
        ret = os.path.join(self.repo_path, 'urls')
        try:
            os.mkdir(ret)
        except:
            pass
        with open(os.path.join(ret, '__init__.py'), 'a') as f:
            pass
        return ret

    @property
    def base_urls_file(self) -> str | None:
        ret = os.path.join(self.base_path, 'urls.py')
        with open(ret, 'r+') as f:
            txt = f.read()
            if txt.find('urlpatterns') == -1:
                f.write(f"from django.urls import path, include\n\n\n"
                        f"app_name = '{self.app_label}'\n"
                        f"urlpatterns = []\n")
        return ret

    @property
    def schemas_path(self) -> str | None:
        ret = os.path.join(self.repo_path, 'schemas')
        try:
            os.mkdir(ret)
        except:
            pass
        with open(os.path.join(ret, '__init__.py'), 'a') as f:
            pass
        return ret

    @property
    def base_schemas_file(self) -> str | None:
        ret = os.path.join(self.base_path, 'schemas.py')
        with open(ret, 'a') as f:
            pass
        return ret

    @property
    def schemas_models_path(self) -> str | None:
        ret = os.path.join(self.schemas_path, 'models')
        try:
            os.mkdir(ret)
        except:
            pass
        with open(os.path.join(ret, '__init__.py'), 'a') as f:
            pass
        return ret

    def schemas_apis_path(self) -> str | None:
        ret = os.path.join(self.schemas_path, 'apis')
        try:
            os.mkdir(ret)
        except:
            pass
        with open(os.path.join(ret, '__init__.py'), 'a') as f:
            pass
        return ret

    __model_name: str | None = None

    @property
    def model_name(self) -> str | None:
        return self.__model_name

    @model_name.setter
    def model_name(self, value: dict):
        tmp: str = value.get('modelname', None)
        if not tmp:
            return
        self.__model_name = casing(tmp, to_case=PASCAL_CASE)

    __app_label: str | None = None

    @property
    def app_label(self) -> str | None:
        return self.__app_label

    @app_label.setter
    def app_label(self, value: dict):
        self.__app_label = value.get('applabel', None)

    def model_name_is_valid(self, rais_exception=True) -> bool:
        if not self.app_label:
            if rais_exception:
                raise CommandError('')
            return False

        if not self.model_name:
            if rais_exception:
                raise CommandError('')
            return False

        try:
            from django.apps import apps

            apps.get_model(app_label=self.app_label, model_name=self.model_name)
            if rais_exception:
                raise CommandError('')
            return False
        except:
            return True

    def initial_model(self):
        model_file_name = f'__{self.model_name_file}'

        model_file_path = os.path.join(self.models_path, f'{model_file_name}.py')
        with open(model_file_path, 'w') as f:
            f.write(f'from django.db import models\n\n\nclass {self.model_name}(models.Model):\n    pass\n')

        models_init_file_path = os.path.join(self.models_path, '__init__.py')
        with open(models_init_file_path, 'a') as f:
            f.write(f'\nfrom .{model_file_name} import {self.model_name} as {self.model_name}Model\n')

        with open(self.base_models_file, 'a') as f:
            f.write(f'\nfrom .repo.models import {self.model_name}Model\n')

    def initial_admin(self):
        admin_file_name = f'__{self.model_name_file}'

        admin_file_path = os.path.join(self.admin_path, f'{admin_file_name}.py')
        with open(admin_file_path, 'w') as f:
            f.write(f"from django.contrib import admin\n\n"
                    f"from {self.app_label}.models import {self.model_name}Model as Model\n\n\n"
                    f"@admin.register(Model)\n"
                    f"class {self.model_name}(admin.ModelAdmin):\n    pass\n")

        admin_init_file_path = os.path.join(self.admin_path, '__init__.py')
        with open(admin_init_file_path, 'a') as f:
            f.write(f'\nfrom .{admin_file_name} import {self.model_name} as {self.model_name}Admin\n')

        with open(self.base_admin_file, 'a') as f:
            f.write(f'\nfrom .repo.admin import {self.model_name}Admin\n')

    def initial_serializers(self):
        serializers_directory_name = f'{self.model_name_file}'
        serializers_directory_path = os.path.join(self.serializers_path, f'{serializers_directory_name}')
        try:
            os.mkdir(serializers_directory_path)
        except:
            pass

        with open(os.path.join(serializers_directory_path, '__base.py'), 'w') as f:
            f.write(f"from rest_framework.serializers import ModelSerializer\n\n"
                    f"from {self.app_label}.models import {self.model_name}Model as Model\n\n\n"
                    f"class Base(ModelSerializer):\n    class Meta:\n        model = Model\n        fields = '__all__'\n")

        with open(os.path.join(serializers_directory_path, '__create.py'), 'w') as f:
            f.write(f"from .__base import Base\n\n\nclass Create(Base):\n    pass\n")

        with open(os.path.join(serializers_directory_path, '__list.py'), 'w') as f:
            f.write(f"from .__base import Base\n\n\nclass List(Base):\n    pass\n")

        with open(os.path.join(serializers_directory_path, '__retrieve.py'), 'w') as f:
            f.write(f"from .__base import Base\n\n\nclass Retrieve(Base):\n    pass\n")

        with open(os.path.join(serializers_directory_path, '__update.py'), 'w') as f:
            f.write(f"from .__base import Base\n\n\nclass Update(Base):\n    pass\n")

        with open(os.path.join(serializers_directory_path, '__destroy.py'), 'w') as f:
            f.write(f"from .__base import Base\n\n\nclass Destroy(Base):\n    pass\n")

        serializers_init_file_path = os.path.join(serializers_directory_path, '__init__.py')
        with open(serializers_init_file_path, 'a') as f:
            f.write(f"from .__create import Create as {self.model_name}CreateSerializer\n"
                    f"from .__list import List as {self.model_name}ListSerializer\n"
                    f"from .__retrieve import Retrieve as {self.model_name}RetrieveSerializer\n"
                    f"from .__update import Update as {self.model_name}UpdateSerializer\n"
                    f"from .__destroy import Destroy as {self.model_name}DestroySerializer\n")
        with open(self.base_serializers_file, 'a') as f:
            f.write(f"\nfrom .repo.serializers.{self.model_name_file} import (\n"
                    f"    {self.model_name}CreateSerializer,\n"
                    f"    {self.model_name}ListSerializer,\n"
                    f"    {self.model_name}RetrieveSerializer,\n"
                    f"    {self.model_name}UpdateSerializer,\n"
                    f"    {self.model_name}DestroySerializer,\n)\n")

    def initial_views(self):
        views_directory_name = f'{self.model_name_file}'
        views_directory_path = os.path.join(self.views_path, f'{views_directory_name}')
        try:
            os.mkdir(views_directory_path)
        except:
            pass

        with open(os.path.join(views_directory_path, '__base.py'), 'w') as f:
            f.write(f"from {self.app_label}.models import {self.model_name}Model as Model\n\n\n"
                    f"class Base:\n"
                    f"    queryset = Model.objects.all()\n")

        with open(os.path.join(views_directory_path, '__create.py'), 'w') as f:
            f.write(f"from rest_framework.generics import CreateAPIView as APIView\n\n"
                    f"from {self.app_label}.serializers import {self.model_name}CreateSerializer as Serializer\n\n"
                    f"from .__base import Base\n\n\n"
                    f"class Create(Base, APIView):\n"
                    f"    serializer_class = Serializer\n")

        with open(os.path.join(views_directory_path, '__list.py'), 'w') as f:
            f.write(f"from django_filters.rest_framework import DjangoFilterBackend\n\n"
                    f"from rest_framework.filters import SearchFilter, OrderingFilter\n"
                    f"from rest_framework.generics import ListAPIView as APIView\n\n"
                    f"from {self.app_label}.serializers import {self.model_name}ListSerializer as Serializer\n\n"
                    f"from .__base import Base\n\n\n"
                    f"class List(Base, APIView):\n"
                    f"    serializer_class = Serializer\n"
                    f"    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)\n")

        with open(os.path.join(views_directory_path, '__retrieve.py'), 'w') as f:
            f.write(f"from rest_framework.generics import RetrieveAPIView as APIView\n\n"
                    f"from {self.app_label}.serializers import {self.model_name}RetrieveSerializer as Serializer\n\n"
                    f"from .__base import Base\n\n\n"
                    f"class Retrieve(Base, APIView):\n"
                    f"    serializer_class = Serializer\n"
                    f"    lookup_field = 'pk'\n")

        with open(os.path.join(views_directory_path, '__update.py'), 'w') as f:
            f.write(f"from rest_framework.generics import UpdateAPIView as APIView\n\n"
                    f"from {self.app_label}.serializers import {self.model_name}UpdateSerializer as Serializer\n\n"
                    f"from .__base import Base\n\n\n"
                    f"class Update(Base, APIView):\n"
                    f"    serializer_class = Serializer\n"
                    f"    lookup_field = 'pk'\n")

        with open(os.path.join(views_directory_path, '__destroy.py'), 'w') as f:
            f.write(f"from rest_framework.generics import DestroyAPIView as APIView\n\n"
                    f"from {self.app_label}.serializers import {self.model_name}DestroySerializer as Serializer\n\n"
                    f"from .__base import Base\n\n\n"
                    f"class Destroy(Base, APIView):\n"
                    f"    serializer_class = Serializer\n"
                    f"    lookup_field = 'pk'\n")

        views_init_file_path = os.path.join(views_directory_path, '__init__.py')
        with open(views_init_file_path, 'a') as f:
            f.write(f"from .__create import Create as {self.model_name}CreateAPIView\n"
                    f"from .__list import List as {self.model_name}ListAPIView\n"
                    f"from .__retrieve import Retrieve as {self.model_name}RetrieveAPIView\n"
                    f"from .__update import Update as {self.model_name}UpdateAPIView\n"
                    f"from .__destroy import Destroy as {self.model_name}DestroyAPIView\n")
        with open(self.base_views_file, 'a') as f:
            f.write(f"\nfrom .repo.views.{self.model_name_file} import (\n"
                    f"    {self.model_name}CreateAPIView,\n"
                    f"    {self.model_name}ListAPIView,\n"
                    f"    {self.model_name}RetrieveAPIView,\n"
                    f"    {self.model_name}UpdateAPIView,\n"
                    f"    {self.model_name}DestroyAPIView,\n)\n")

    def initial_urlpatterns(self):
        urls_file_name = f'{self.model_name_file}'
        urls_file_path = os.path.join(self.urls_path, f'{urls_file_name}')

        with open(f'{urls_file_path}.py', 'w') as f:
            f.write(f"from django.urls import path\n\n"
                    f"from {self.app_label}.views import (\n"
                    f"    {self.model_name}CreateAPIView as CreateAPIView,\n"
                    f"    {self.model_name}ListAPIView as ListAPIView,\n"
                    f"    {self.model_name}RetrieveAPIView as RetrieveAPIView,\n"
                    f"    {self.model_name}UpdateAPIView as UpdateAPIView,\n"
                    f"    {self.model_name}DestroyAPIView as DestroyAPIView,\n"
                    f")\n\n\n"
                    f"app_name = '{self.model_name_file}s'\n"
                    f"urlpatterns = [\n"
                    f"    path('', CreateAPIView.as_view(), name='create'),\n"
                    f"    path('', ListAPIView.as_view(), name='list'),\n"
                    f"    path('<int:pk>/', RetrieveAPIView.as_view(), name='retrieve'),\n"
                    f"    path('<int:pk>/', UpdateAPIView.as_view(), name='update'),\n"
                    f"    path('<int:pk>/', DestroyAPIView.as_view(), name='destroy'),\n"
                    f"]\n")
        with open(self.base_urls_file, 'r') as f:
            txt = f.read()
        with open(self.base_urls_file, 'w') as f:
            tmp = (f"{txt[:txt.find(']')]}\n"
                   f"\n    path('{casing(self.model_name, to_case=KEBAB_CASE)}s/', "
                   f"include('{self.app_label}.repo.urls.{self.model_name_file}')),\n"
                   f"{txt[txt.find(']'):]}")
            f.write(tmp)

    @property
    def model_name_file(self):
        return casing(self.model_name, to_case=CAMEL_CASE)

    @staticmethod
    def convert_to_pascal_case(value: str):
        tmp = ''
        uppercase = False
        for i, c in enumerate(value):
            if c == '_':
                uppercase = True
                continue
            if i == 0:
                tmp += c.upper()
                continue
            if uppercase:
                tmp += c.upper()
                uppercase = False
                continue
            tmp += c
        ret = tmp
        return ret

    @staticmethod
    def convert_to_snake_case(value: str):
        tmp = ''
        for c in value:
            if c.isupper():
                tmp += '_' + c.lower()
                continue
            tmp += c
        ret = tmp
        return ret
