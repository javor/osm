import copy
import traceback

import docker
from django.conf import settings
from django.core.management import BaseCommand
from docker.errors import APIError
from docker.errors import NotFound

from core.management.utils.options import OptionsReader
from core.management.utils.options import OptionsReaderException


class Command(BaseCommand):  # TODO: Add tests
    _default_fields = ('db_name',)

    help = 'Stops PostgreSQL container instance'

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

    def handle(self, *args, **options):
        try:
            self._try_handle(options)
        except (APIError, NotFound, OptionsReaderException) as e:
            self.stdout.write('Cannot stop database container: {0}'.format(str(e)))
        except Exception as e:
            self.stdout.write(''.format(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))

    @staticmethod
    def _try_handle(options):
        dbs = copy.deepcopy(settings.DATABASES)
        docker_params = OptionsReader.prepare_options(dbs, options, Command._default_fields)
        client = docker.from_env()
        client.containers.get(docker_params['name']).stop()
        client.containers.get(docker_params['name']).remove()
