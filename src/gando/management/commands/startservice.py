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


class BasePackageInfo:
    def __init__(self, path: str):
        self.path: str = path
        self.initial_path: str = os.path.join(self.path, '__init__.py')


class BasePackages:
    def __init__(self, application_path: str):
        self.repo: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=application_path, name='repo'))
        self.repo__schemas: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo.path, name='schemas'))
        self.repo__schemas__services: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo__schemas.path, name='services'))
        self.repo__services: BasePackageInfo = BasePackageInfo(
            path=package_maker(parent_path=self.repo.path, name='services'))


class Command(BaseCommand):
    help = ("This command helps us to automatically create the basic prerequisites of "
            "this service when we define a service, so that we can personalize each of "
            "the tools that are created automatically if needed.")

    def add_arguments(self, parser):
        """
        This command has two mandatory arguments so that we can automatically create
        the prerequisites for each service.
        -al or --applabel: This argument is used to get the name of the desired application.
        -sn or --servicename: And this argument also specifies the name of the service inside that application.
        """
        parser.add_argument(
            '-al', '--applabel', type=str,
            help='This argument is used to get the name of the desired application.')
        parser.add_argument(
            '-sn', '--servicename', type=str,
            help='This argument also specifies the name of the service inside that application.')

    def handle(self, *args, **kwargs):
        # First, we get the value of the set parameters from the sent command.
        self.app_label = kwargs
        self.service_name = kwargs

        # Here we check the acceptability of the received parameters.
        self.service_name_is_valid(rais_exception=True)

        # set Application path
        self.application_path = kwargs

        # set Base Packages path
        self.base_packages = BasePackages(application_path=self.application_path)

        self.initial_service()

        self.initial_schemas()

    __service_name: str | None = None

    @property
    def service_name(self) -> str | None:
        return self.__service_name

    @service_name.setter
    def service_name(self, value: dict):
        tmp = value.get('servicename', None)
        if tmp:
            self.__service_name = casing(tmp, to_case=PASCAL_CASE)

    @property
    def service_name_snake_case(self):
        return casing(self.service_name)

    __app_label: str | None = None

    @property
    def app_label(self) -> str | None:
        return self.__app_label

    @app_label.setter
    def app_label(self, value: dict):
        self.__app_label = value.get('applabel', None)

    def service_name_is_valid(self, rais_exception=True) -> bool:
        if not self.app_label:
            if rais_exception:
                raise CommandError(
                    "The name of the application is not entered, "
                    "which is actually the same as the -al or --applabel argument. "
                    "It is not set. Please check and fix the error and try again.")
            return False

        if not self.service_name:
            if rais_exception:
                raise CommandError(
                    "The service name is not entered, "
                    "which is actually the same as the -mn or --servicename argument. "
                    "It is not set. Please check and fix the error and try again.")
            return False

        return True

    def service_is_exist(self) -> bool:
        try:
            from django.apps import apps

            apps.get_service(app_label=self.app_label, service_name=self.service_name)
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

    base_packages: BasePackages | None = None

    def initial_service(self):
        file_path = python_file_maker(self.base_packages.repo__services.path, self.service_name, private_=False)

        with open(file_path, 'w') as f:
            f.write(
                f"from gando.architectures.services import BaseService"
                f"\n"
                f"\n"
                f"\n"
                f"class {self.service_name}Service(BaseService):"
                f"\n"
                f"    def __init__(self, *args, **kwargs):"
                f"\n"
                f"        super().__init__(*args, **kwargs)"
                f"\n"
                f"\n"
                f"    def service_output_handler(self, *args, **kwargs):"
                f"\n"
                f"        return True"
                f"\n"
            )

    def initial_schemas(self):
        package_maker(
            self.base_packages.repo__schemas__services.path, self.service_name_snake_case)

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
