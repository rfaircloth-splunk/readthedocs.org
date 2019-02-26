"""Containerized environment settings."""
from __future__ import absolute_import
import os

from .base import CommunityBaseSettings


_redis_host = os.getenv('REDIS_HOST', 'redis')
_redis_port = os.getenv('REDIS_PORT', '6379')
_redis_db = os.getenv('REDIS_DB', '0')
_elastic_host = os.getenv('ELASTIC_HOST', 'elasticsearch')
_elastic_port = os.getenv('ELASTIC_PORT', '9200')


class ContainerSettings(CommunityBaseSettings):
    #
    """Settings for containerized environment"""
    @property
    def LOGGING(self):  # noqa - avoid pep8 N802
        logging = super().LOGGING
        logging['formatters']['default']['format'] = '[%(asctime)s] ' + \
            self.LOG_FORMAT
        # Allow Sphinx and other tools to create loggers
        logging['disable_existing_loggers'] = False
        return logging

    DEBUG = os.getenv('RTD_DEBUG', 'false').lower() == 'true'

    SITE_ROOT = '/opt/rtfd'
    # Set this to the root domain where this RTD installation will be running
    PRODUCTION_DOMAIN = os.getenv('RTD_PRODUCTION_DOMAIN', 'localhost:8000')
    PUBLIC_DOMAIN = os.getenv('RTD_PUBLIC_DOMAIN', PRODUCTION_DOMAIN)
    USE_SUBDOMAIN = os.getenv('RTD_USE_SUBDOMAIN', 'false').lower() == 'true'
    WEBSOCKET_HOST = os.getenv('RTD_WEBSOCKET_HOST', 'localhost:8088')

    @property
    def DATABASES(self):  # noqa
        print("RTD_HAS_DATABASE: {0}\n".format(
            os.getenv('RTD_HAS_DATABASE', 'false').lower()))
        if os.getenv('RTD_HAS_DATABASE', 'false').lower() == 'true':
            return {
                'default': {
                    'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql_psycopg2'),
                    'NAME': os.getenv('DB_NAME', 'readthedocs'),
                    'USER': os.getenv('DB_USER', 'rtd'),
                    'PASSWORD': os.getenv('DB_PASS', 'rtd'),
                    'HOST': os.getenv('DB_HOST', 'database'),
                    'PORT': os.getenv('DB_PORT', 5432),
                }
            }
        else:
            return {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(self.SITE_ROOT, 'container.db'),
                }
            }

    DONT_HIT_DB = False

    # Email
    DEFAULT_FROM_EMAIL = os.getenv(
        'RTD_DEFAULT_FROM_EMAIL', 'no-reply@{}'.format(PRODUCTION_DOMAIN))

    # Turn off email verification

    ACCOUNT_EMAIL_VERIFICATION = os.getenv(
        'RTD_ACCOUNT_EMAIL_VERIFICATION', 'none')
    SESSION_COOKIE_DOMAIN = os.getenv('RTD_SESSION_COOKIE_DOMAIN', None)

    CACHE_BACKEND = 'dummy://'

    AUTHENTICATION_BACKENDS = CommunityBaseSettings.AUTHENTICATION_BACKENDS + \
        ('guardian.backends.ObjectPermissionBackend', )

    SLUMBER_USERNAME = os.getenv('RTD_SLUMBER_USERNAME', 'slumber')
    SLUMBER_PASSWORD = os.getenv('RTD_SLUMBER_PASSWORD', 'slumber')
    SLUMBER_API_HOST = os.getenv(
        'RTD_SLUMBER_API_HOST', 'http://localhost:8000')
    SLUMBER_EMAIL = os.getenv(
        'RTD_SLUMBER_EMAIL', '{0}@localhost'.format(SLUMBER_USERNAME))

    @property
    def CACHE(self):  # noqa
        if os.getenv('RTD_USE_REDIS_FOR_CACHE', 'false').lower() == 'true':
            return {
                'default': {
                    'BACKEND': 'redis_cache.RedisCache',
                    'LOCATION': 'redis://{0}:{1}/{2}'.format(_redis_host, _redis_port, _redis_db),
                    'OPTIONS': {
                        'PARSER_CLASS': 'redis.connection.HiredisParser',
                    },
                },
            }
        else:
            return {
                'default': {
                    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                    'PREFIX': 'docs',
                }
            }

    BROKER_URL = 'redis://{0}:{1}/{2}'.format(
        _redis_host, _redis_port, _redis_db)

    CELERY_RESULT_BACKEND = 'redis://{0}:{1}/{2}'.format(
        _redis_host, _redis_port, _redis_db)
    CELERY_RESULT_SERIALIZER = 'json'

    CELERY_ALWAYS_EAGER = True
    CELERY_TASK_IGNORE_RESULT = False

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    FILE_SYNCER = 'readthedocs.builds.syncers.LocalSyncer'

    # Users
    ADMIN_USERNAME = os.getenv('RTD_ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('RTD_ADMIN_PASSWORD', 'admin')
    ADMIN_EMAIL = os.getenv('RTD_ADMIN_EMAIL', '{0}@{1}'.format(
        ADMIN_USERNAME, '.'.join(PRODUCTION_DOMAIN.split('.')[-2:])))

    ADMINS = ((os.getenv('RTD_ADMIN_NAME', 'RTD Admin'), ADMIN_EMAIL), )

    GLOBAL_ANALYTICS_CODE = os.getenv('RTD_GLOBAL_ANALYTICS_CODE', '')

    # Enable private Git repositories
    ALLOW_PRIVATE_REPOS = os.getenv(
        'RTD_ALLOW_PRIVATE_REPOS', 'false').lower() == 'true'
    SERVE_DOCS = ['private']

    USE_PROMOS = False

    # For testing locally. Put this in your /etc/hosts:
    # 127.0.0.1 test
    # and navigate to http://test:8000
#   CORS_ORIGIN_WHITELIST = (
#        'test:8000',
#    )

    ES_HOSTS = ['{0}:{1}'.format(_elastic_host,
                                 _elastic_port)]

    ELASTICSEARCH_DSL = {
        'default': {
            'hosts': '{0}:{1}'.format(_elastic_host,
                                      _elastic_port)
        },
    }

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ["/opt/rtfd/readthedocs/templates_custom",
                     "/opt/rtfd/readthedocs/templates"],
            'OPTIONS': {
                'debug': DEBUG,
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.request',
                    # Read the Docs processor
                    'readthedocs.core.context_processors.readthedocs_processor',
                ],
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ],
            },
        },
    ]


ContainerSettings.load_settings(__name__)
