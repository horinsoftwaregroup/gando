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
        self.urls: str = python_file_maker(path=application_path, name='urls')


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
        self.repo__schemas__services: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo__schemas.path, name='services'))
        self.repo__urls: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo.path, name='urls'))
        self.repo__services: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo.path, name='services'))
        self.repo__interfaces: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo.path, name='interfaces'))
        self.repo__apis: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo.path, name='apis'))


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

        i_fp = self.base_packages.repo__models.initial_path
        with open(i_fp, 'a') as f:
            f.write(
                f"{self.__new_line(i_fp)}"
                f"from .__{self.model_name_snake_case} import {self.model_name} as {self.model_name}Model"
                f"\n"
            )

        m_fp = self.base_files.models
        with open(m_fp, 'a') as f:
            f.write(
                f"{self.__new_line(m_fp)}"
                f"from .repo.models import {self.model_name}Model"
                f"\n"
            )

    def initial_admin(self):
        file_path = python_file_maker(self.base_packages.repo__admin.path, self.model_name, private_=True)

        with open(file_path, 'w') as f:
            f.write(
                f"from django.contrib import admin\n\n"
                f"from {self.app_label}.models import {self.model_name}Model as Model\n\n\n"
                f"@admin.register(Model)\n"
                f"class {self.model_name}Admin(admin.ModelAdmin):\n    pass\n"
            )

        i_fp = self.base_packages.repo__admin.initial_path
        with open(i_fp, 'a') as f:
            f.write(
                f"{self.__new_line(i_fp)}"
                f"from .__{self.model_name_snake_case} import {self.model_name}Admin"
                f"\n"
            )

        a_fp = self.base_files.admin
        with open(a_fp, 'a') as f:
            f.write(
                f"{self.__new_line(a_fp)}"
                f"from .repo.admin import {self.model_name}Admin"
                f"\n"
            )

    def initial_urlpatterns(self):
        file_path = python_file_maker(self.base_packages.repo__urls.path, self.model_name)

        with open(file_path, 'w') as f:
            f.write(
                f"from django.urls import path\n\n"
                f"app_name = '{self.model_name_snake_case}s'\n"
                f"urlpatterns = [\n"
                f"    # path('', SampleAPI.as_view(), name='sample'),\n"
                f"]\n"
            )

        default_txt = (
            f"from django.urls import path, include\n\n\n"
            f"app_name = '{self.app_label}'\n"
            f"urlpatterns = [\n"
            f"]\n"
        )
        u_fp = self.base_files.urls
        if self.__find_in_file(u_fp, 'urlpatterns') is not None:
            txt = self.__file_content(u_fp)
        else:
            txt = default_txt
        with open(self.base_files.urls, 'w') as f:
            f.write(
                f"{txt[:txt.find(']')]}"
                f"\n"
                f"    path('{casing(self.model_name, to_case=KEBAB_CASE)}s/', "
                f"include('{self.app_label}.repo.urls.{self.model_name_snake_case}')),"
                f"\n"
                f"{txt[txt.find(']'):]}"
            )

    def initial_schemas(self):
        file_path = python_file_maker(self.base_packages.repo__schemas__models.path, self.model_name, private_=True)
        with open(file_path, 'w') as f:
            f.write(
                f"from pydantic import BaseModel\n\n\n"
                f"class {self.model_name}ModelSchema(BaseModel):\n"
                f"    id: int | None = None\n"
            )

        i_fp = self.base_packages.repo__schemas__models.initial_path
        with open(i_fp, 'a') as f:
            f.write(
                f"{self.__new_line(i_fp)}"
                f"from .__{self.model_name_snake_case} import {self.model_name}ModelSchema"
                f"\n"
            )

    @staticmethod
    def __new_line(file_name):
        tmp = ''
        with open(file_name, 'r') as f:
            lines = f.read()
            if lines[-1] != '\n':
                tmp = '\n'

        ret = tmp
        return ret

    @staticmethod
    def __find_in_file(file_name, sub):
        tmp = ''
        with open(file_name, 'r') as f:
            txt = f.read()
            if txt.find(sub) == -1:
                tmp = None

        ret = tmp
        return ret

    @staticmethod
    def __file_content(file_name, default=''):
        tmp = default
        with open(file_name, 'r') as f:
            txt = f.read()
            if len(txt) != 0:
                tmp = str(txt)

        ret = tmp
        return ret
