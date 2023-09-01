from pathlib import Path
import os
from pydantic import BaseModel as BaseSchema

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from gando.utils.strings.converters import casing
from gando.utils.strings.casings import PASCAL_CASE, KEBAB_CASE

# definitions
PROJECT_PATH = settings.BASE_DIR


# tools
def package_maker(parent_path: str, name: str) -> str:
    package_path = os.path.join(parent_path, casing(name))
    if not os.path.exists(package_path):
        os.mkdir(package_path)

    package_init = os.path.join(package_path, '__init__.py')
    if not os.path.exists(package_init):
        Path(package_init).touch()

    return package_path


def python_file_maker(path: str, name: str, private_=False) -> str:
    name = casing(f'{"__" if private_ else ""}{name.split(".")[0]}')
    python_file_full_name = os.path.join(path, f'{name}.py')
    if not os.path.exists(python_file_full_name):
        Path(python_file_full_name).touch()

    return python_file_full_name


class BaseFiles:
    def __init__(self, application_path: str):
        self.admin: str = python_file_maker(path=application_path, name='admin')
        self.models: str = python_file_maker(path=application_path, name='models')
        self.schemas: str = python_file_maker(path=application_path, name='schemas')
        self.serializers: str = python_file_maker(path=application_path, name='serializers')
        self.urls: str = python_file_maker(path=application_path, name='urls')
        self.views: str = python_file_maker(path=application_path, name='views')


class BasePackageInfo:
    def __init__(self, path: str):
        self.path: str = path
        self.initial_path: str = os.path.join(self.path, '__init__.py')


class BasePackages:
    def __init__(self, application_path: str):
        self.repo: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=application_path, name='repo'))
        self.repo__admin: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo.path, name='admin'))
        self.repo__models: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo.path, name='models'))
        self.repo__schemas: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo.path, name='schemas'))
        self.repo__schemas__models: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo__schemas.path, name='models'))
        self.repo__schemas__apis: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo__schemas.path, name='apis'))
        self.repo__serializers: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo.path, name='serializers'))
        self.repo__urls: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo.path, name='urls'))
        self.repo__views: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo.path, name='views'))


class Command(BaseCommand):
    help = ("This command helps us to automatically create the basic prerequisites of "
            "this model when we define a model, so that we can personalize each of "
            "the tools that are created automatically if needed.")

    def add_arguments(self, parser):
        """
        This command has two mandatory arguments so that we can automatically create
        the prerequisites for each model.
        -al or --applabel: This argument is used to get the name of the desired application.
        -mn or --modelname: And this argument also specifies the name of the model inside that application.
        """
        parser.add_argument(
            '-al', '--applabel', type=str,
            help='This argument is used to get the name of the desired application.')
        parser.add_argument(
            '-mn', '--modelname', type=str,
            help='This argument also specifies the name of the model inside that application.')

    def handle(self, *args, **kwargs):
        # First, we get the value of the set parameters from the sent command.
        self.app_label = kwargs
        self.model_name = kwargs

        # Here we check the acceptability of the received parameters.
        self.model_name_is_valid(rais_exception=True)

        # set Application path
        self.application_path = kwargs

        # set Base Files path
        self.base_files = BaseFiles(application_path=self.application_path)
        # set Base Packages path
        self.base_packages = BasePackages(application_path=self.application_path)

        self.initial_model()

        self.initial_admin()
        self.initial_serializers()
        self.initial_views()
        self.initial_urlpatterns()
        self.initial_schemas()

    __model_name: str | None = None

    @property
    def model_name(self) -> str | None:
        return self.__model_name

    @model_name.setter
    def model_name(self, value: dict):
        tmp = value.get('modelname', None)
        if tmp:
            self.__model_name = casing(tmp, to_case=PASCAL_CASE)

    @property
    def model_name_snake_case(self):
        return casing(self.model_name)

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
                raise CommandError(
                    "The name of the application is not entered, "
                    "which is actually the same as the -al or --applabel argument. "
                    "It is not set. Please check and fix the error and try again.")
            return False

        if not self.model_name:
            if rais_exception:
                raise CommandError(
                    "The model name is not entered, "
                    "which is actually the same as the -mn or --modelname argument. "
                    "It is not set. Please check and fix the error and try again.")
            return False

        return True

    def model_is_exist(self) -> bool:
        try:
            from django.apps import apps

            apps.get_model(app_label=self.app_label, model_name=self.model_name)
            return True
        except:
            return False

    __application_path: str | None = None

    @property
    def application_path(self) -> str | None:
        return self.__application_path

    @application_path.setter
    def application_path(self, value: dict):
        self.__application_path = os.path.join(PROJECT_PATH, value.get('applabel'))

    base_files: BaseFiles | None = None
    base_packages: BasePackages | None = None

    def initial_model(self):
        file_path = python_file_maker(self.base_packages.repo__models.path, self.model_name, private_=True)

        with open(file_path, 'w') as f:
            f.write(f'from django.db import models\n\n\nclass {self.model_name}(models.Model):\n    pass\n')

        with open(self.base_packages.repo__models.initial_path, 'a') as f:
            f.write(f'\nfrom .__{self.model_name_snake_case} import {self.model_name} as {self.model_name}Model\n')

        with open(self.base_files.models, 'a') as f:
            f.write(f'\nfrom .repo.models import {self.model_name}Model\n')

    def initial_admin(self):
        file_path = python_file_maker(self.base_packages.repo__admin.path, self.model_name, private_=True)

        with open(file_path, 'w') as f:
            f.write(f"from django.contrib import admin\n\n"
                    f"from {self.app_label}.models import {self.model_name}Model as Model\n\n\n"
                    f"@admin.register(Model)\n"
                    f"class {self.model_name}(admin.ModelAdmin):\n    pass\n")

        with open(self.base_packages.repo__admin.initial_path, 'a') as f:
            f.write(f'\nfrom .__{self.model_name_snake_case} import {self.model_name} as {self.model_name}Admin\n')

        with open(self.base_files.admin, 'a') as f:
            f.write(f'\nfrom .repo.admin import {self.model_name}Admin\n')

    def initial_serializers(self):
        dir_path = package_maker(self.base_packages.repo__serializers.path, self.model_name)

        with open(os.path.join(dir_path, '__base.py'), 'w') as f:
            f.write(f"from rest_framework.serializers import ModelSerializer\n\n"
                    f"from {self.app_label}.models import {self.model_name}Model as Model\n\n\n"
                    f"class Base(ModelSerializer):\n"
                    f"    class Meta:\n"
                    f"        model = Model\n"
                    f"        fields = '__all__'\n")

        with open(os.path.join(dir_path, '__create.py'), 'w') as f:
            f.write(f"from .__base import Base\n\n\nclass Create(Base):\n    pass\n")

        with open(os.path.join(dir_path, '__list.py'), 'w') as f:
            f.write(f"from .__base import Base\n\n\nclass List(Base):\n    pass\n")

        with open(os.path.join(dir_path, '__retrieve.py'), 'w') as f:
            f.write(f"from .__base import Base\n\n\nclass Retrieve(Base):\n    pass\n")

        with open(os.path.join(dir_path, '__update.py'), 'w') as f:
            f.write(f"from .__base import Base\n\n\nclass Update(Base):\n    pass\n")

        with open(os.path.join(dir_path, '__destroy.py'), 'w') as f:
            f.write(f"from .__base import Base\n\n\nclass Destroy(Base):\n    pass\n")

        with open(os.path.join(dir_path, '__init__.py'), 'a') as f:
            f.write(f"from .__create import Create as {self.model_name}CreateSerializer\n"
                    f"from .__list import List as {self.model_name}ListSerializer\n"
                    f"from .__retrieve import Retrieve as {self.model_name}RetrieveSerializer\n"
                    f"from .__update import Update as {self.model_name}UpdateSerializer\n"
                    f"from .__destroy import Destroy as {self.model_name}DestroySerializer\n")

        with open(self.base_files.serializers, 'a') as f:
            f.write(f"\nfrom .repo.serializers.{self.model_name_snake_case} import (\n"
                    f"    {self.model_name}CreateSerializer,\n"
                    f"    {self.model_name}ListSerializer,\n"
                    f"    {self.model_name}RetrieveSerializer,\n"
                    f"    {self.model_name}UpdateSerializer,\n"
                    f"    {self.model_name}DestroySerializer,\n)\n")

    def initial_views(self):
        dir_path = package_maker(self.base_packages.repo__views.path, self.model_name)

        with open(os.path.join(dir_path, '__base.py'), 'w') as f:
            f.write(f"from {self.app_label}.models import {self.model_name}Model as Model\n\n\n"
                    f"class Base:\n"
                    f"    queryset = Model.objects.all()\n")

        with open(os.path.join(dir_path, '__create.py'), 'w') as f:
            f.write(f"from rest_framework.generics import CreateAPIView as APIView\n\n"
                    f"from {self.app_label}.serializers import {self.model_name}CreateSerializer as Serializer\n\n"
                    f"from .__base import Base\n\n\n"
                    f"class Create(Base, APIView):\n"
                    f"    serializer_class = Serializer\n")

        with open(os.path.join(dir_path, '__list.py'), 'w') as f:
            f.write(f"from django_filters.rest_framework import DjangoFilterBackend\n\n"
                    f"from rest_framework.filters import SearchFilter, OrderingFilter\n"
                    f"from rest_framework.generics import ListAPIView as APIView\n\n"
                    f"from {self.app_label}.serializers import {self.model_name}ListSerializer as Serializer\n\n"
                    f"from .__base import Base\n\n\n"
                    f"class List(Base, APIView):\n"
                    f"    serializer_class = Serializer\n"
                    f"    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)\n")

        with open(os.path.join(dir_path, '__retrieve.py'), 'w') as f:
            f.write(f"from rest_framework.generics import RetrieveAPIView as APIView\n\n"
                    f"from {self.app_label}.serializers import {self.model_name}RetrieveSerializer as Serializer\n\n"
                    f"from .__base import Base\n\n\n"
                    f"class Retrieve(Base, APIView):\n"
                    f"    serializer_class = Serializer\n"
                    f"    lookup_field = 'pk'\n")

        with open(os.path.join(dir_path, '__update.py'), 'w') as f:
            f.write(f"from rest_framework.generics import UpdateAPIView as APIView\n\n"
                    f"from {self.app_label}.serializers import {self.model_name}UpdateSerializer as Serializer\n\n"
                    f"from .__base import Base\n\n\n"
                    f"class Update(Base, APIView):\n"
                    f"    serializer_class = Serializer\n"
                    f"    lookup_field = 'pk'\n")

        with open(os.path.join(dir_path, '__destroy.py'), 'w') as f:
            f.write(f"from rest_framework.generics import DestroyAPIView as APIView\n\n"
                    f"from {self.app_label}.serializers import {self.model_name}DestroySerializer as Serializer\n\n"
                    f"from .__base import Base\n\n\n"
                    f"class Destroy(Base, APIView):\n"
                    f"    serializer_class = Serializer\n"
                    f"    lookup_field = 'pk'\n")

        with open(os.path.join(dir_path, '__init__.py'), 'a') as f:
            f.write(f"from .__create import Create as {self.model_name}CreateAPIView\n"
                    f"from .__list import List as {self.model_name}ListAPIView\n"
                    f"from .__retrieve import Retrieve as {self.model_name}RetrieveAPIView\n"
                    f"from .__update import Update as {self.model_name}UpdateAPIView\n"
                    f"from .__destroy import Destroy as {self.model_name}DestroyAPIView\n")

        with open(self.base_files.views, 'a') as f:
            f.write(f"\nfrom .repo.views.{self.model_name_snake_case} import (\n"
                    f"    {self.model_name}CreateAPIView,\n"
                    f"    {self.model_name}ListAPIView,\n"
                    f"    {self.model_name}RetrieveAPIView,\n"
                    f"    {self.model_name}UpdateAPIView,\n"
                    f"    {self.model_name}DestroyAPIView,\n)\n")

    def initial_urlpatterns(self):
        file_path = python_file_maker(self.base_packages.repo__urls.path, self.model_name)

        with open(file_path, 'w') as f:
            f.write(f"from django.urls import path\n\n"
                    f"from {self.app_label}.views import (\n"
                    f"    {self.model_name}CreateAPIView as CreateAPIView,\n"
                    f"    {self.model_name}ListAPIView as ListAPIView,\n"
                    f"    {self.model_name}RetrieveAPIView as RetrieveAPIView,\n"
                    f"    {self.model_name}UpdateAPIView as UpdateAPIView,\n"
                    f"    {self.model_name}DestroyAPIView as DestroyAPIView,\n"
                    f")\n\n\n"
                    f"app_name = '{self.model_name_snake_case}s'\n"
                    f"urlpatterns = [\n"
                    f"    path('', CreateAPIView.as_view(), name='create'),\n"
                    f"    path('', ListAPIView.as_view(), name='list'),\n"
                    f"    path('<int:pk>/', RetrieveAPIView.as_view(), name='retrieve'),\n"
                    f"    path('<int:pk>/', UpdateAPIView.as_view(), name='update'),\n"
                    f"    path('<int:pk>/', DestroyAPIView.as_view(), name='destroy'),\n"
                    f"]\n")

        with open(self.base_files.urls, 'r+') as f:
            txt = f.read()

            if txt.find('urlpatterns') == -1:
                f.write(f"from django.urls import path, include\n\n\n"
                        f"app_name = '{self.app_label}'\n"
                        f"urlpatterns = [\n"
                        f"    path('{casing(self.model_name, to_case=KEBAB_CASE)}s/', "
                        f"include('{self.app_label}.repo.urls.{self.model_name_snake_case}')),\n"
                        f"]\n")
            else:
                f.write('')
                f.write(f"{txt[:txt.find(']')]}\n"
                        f"\n    path('{casing(self.model_name, to_case=KEBAB_CASE)}s/', "
                        f"include('{self.app_label}.repo.urls.{self.model_name_snake_case}')),\n"
                        f"{txt[txt.find(']'):]}")

    def initial_schemas(self):
        file_path = python_file_maker(self.base_packages.repo__schemas__models.path, self.model_name, private_=True)
        with open(file_path, 'w') as f:
            f.write(f"from pydantic import BaseModel\n\n\n"
                    f"class {self.model_name}(BaseModel):\n"
                    f"    id: int | None = None\n"
                    f"    pk: int | None = None\n")

        with open(self.base_packages.repo__schemas__models.initial_path, 'a') as f:
            f.write(
                f"\nfrom .__{self.model_name_snake_case} import {self.model_name} as {self.model_name}ModelSchema\n")

        with open(self.base_files.schemas, 'a') as f:
            f.write(f"\nfrom .repo.schemas.models import {self.model_name}ModelSchema\n")
