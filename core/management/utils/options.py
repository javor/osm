import copy


class OptionsReaderException(ValueError):
    ...


class OptionsReader(object):
    """ TODO: documentation """
    _default_options = {
        'detach': True,  # don't block command if start docker container
        'environment': {},
        'image': 'postgres',
        'restart_policy': {
            "Name": "on-failure",
            "MaximumRetryCount": 5
        }
    }

    @staticmethod
    def prepare_options(databases, options, fields):
        try:
            return OptionsReader._try_prepare_options(
                databases, options, fields
            )
        except AttributeError as e:
            raise OptionsReaderException(str(e))
        except Exception as e:
            raise OptionsReaderException(str(e))

    @staticmethod
    def _try_prepare_options(databases, options, fields):
        params = copy.deepcopy(OptionsReader._default_options)
        db = options['db']
        if 'db_name' in fields:
            db_name = options.get('db_name') or databases.get(db, {}).get('NAME')
            OptionsReader._check_option('db_name', db_name)
            params['name'] = db_name
            params['environment']['POSTGRES_DB'] = db_name

        if 'db_user' in fields:
            db_user = options.get('db_user') or databases.get(db, {}).get('USER')
            OptionsReader._check_option('db_user', db_user)
            params['environment']['POSTGRES_USER'] = db_user

        if 'db_pass' in fields:
            db_pass = options.get('db_pass') or databases.get(db, {}).get('PASSWORD')
            OptionsReader._check_option('db_pass', db_pass)
            params['environment']['POSTGRES_PASSWORD'] = db_pass

        if 'db_port' in fields:
            db_port = options.get('db_port') or databases.get(db, {}).get('PORT')
            params['ports'] = {
                '5432/tcp': db_port if db_port else '5432'
            }

        if 'db_version' in fields:
            db_version = options.get('db_version', ) or databases.get(db, {}).get('VERSION')
            params['image'] = params['image'] + (':{0}'.format(db_version) if db_version else '')

        return params

    @staticmethod
    def _check_option(name, value):
        if value:
            return True

        raise AttributeError(
            'Parameter {0} is not specified either by command or settings file.'.format(name))
