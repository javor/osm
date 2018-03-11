import copy
import traceback

import docker
from django.conf import settings
from django.core.management import BaseCommand
from docker.errors import APIError
from docker.errors import ContainerError
from docker.errors import ImageNotFound

from core.management.utils.options import OptionsReader
from core.management.utils.options import OptionsReaderException


class Command(BaseCommand):  # TODO: Add tests
    _default_fields = ('db_name', 'db_user', 'db_pass', 'db_port', 'db_version')

    help = 'Starts PostgreSQL container instance'

    def add_arguments(self, parser):
        parser.add_argument(
            '--db',
            default='default',
            help='Database config from from settings'
        )
        parser.add_argument(
            '--db-name',
            help='Database name'
        )
        parser.add_argument(
            '--db-user',
            help='Database user name for PostgresSQL container'
        )
        parser.add_argument(
            '--db-pass',
            help='Database user pass for PostgresSQL container'
        )
        parser.add_argument(
            '--db-port',
            help='Database port for PostgresSQL container ports mapping'
        )
        parser.add_argument(
            '--db-version',
            default=settings.DATABASES.get('default', {}).get('VERSION', None),
            help='PostgresSQL version used for create container'
        )

    def handle(self, *args, **options):
        try:
            self._try_handle(options)
        except (APIError, ContainerError, ImageNotFound, OptionsReaderException) as e:
            self.stdout.write('Cannot start database container: {0}'.format(str(e)))
        except Exception as e:
            self.stdout.write(''.format(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))

    @staticmethod
    def _try_handle(options):
        dbs = copy.deepcopy(settings.DATABASES)
        docker_params = OptionsReader.prepare_options(dbs, options, Command._default_fields)
        client = docker.from_env()
        client.containers.run(**docker_params)
