"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from corsheaders.defaults import default_headers
from kombu import Queue, Exchange

from core import __version__

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')

API_INTERNAL_BASE_URL = os.environ.get('API_INTERNAL_BASE_URL', 'http://api:8000')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=q1%fd62$x!35xzzlc3lix3g!s&!2%-1d@5a=rm!n4lu74&6)p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'TRUE'

ALLOWED_HOSTS = ['*']

CORS_ALLOW_HEADERS = default_headers + (
    'INCLUDEFACETS',
)

CORS_EXPOSE_HEADERS = (
    'num_found',
    'num_returned',
    'pages',
    'page_number',
    'next',
    'previous',
    'offset',
    'Content-Length',
    'Content-Range',
    'X-OCL-API-VERSION',
    'X-OCL-REQUEST-USER',
    'X-OCL-RESPONSE-TIME',
    'X-OCL-REQUEST-URL',
    'X-OCL-REQUEST-METHOD',
)

CORS_ORIGIN_ALLOW_ALL = True
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'mozilla_django_oidc',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'django_elasticsearch_dsl',
    'corsheaders',
    'ordered_model',
    'cid.apps.CidAppConfig',
    'health_check',  # required
    'health_check.db',  # stock Django health checkers
    # 'health_check.contrib.celery_ping',  # requires celery
    'health_check.contrib.redis',  # requires Redis broker
    'core.common.apps.CommonConfig',
    'core.users',
    'core.orgs',
    'core.sources.apps.SourceConfig',
    'core.collections',
    'core.concepts',
    'core.mappings',
    'core.importers',
    'core.pins',
    'core.client_configs',
    'core.tasks',
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core.common.authentication.OCLAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'core.common.renderers.ZippedJSONRenderer',
    ),
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'core.common.negotiation.OptionallyCompressContentNegotiation',
}
OIDC_DRF_AUTH_BACKEND = 'core.common.backends.OCLOIDCAuthenticationBackend'
AUTHENTICATION_BACKENDS = (
    'core.common.backends.OCLAuthenticationBackend',
)


SWAGGER_SETTINGS = {
    'PERSIST_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'DOC_EXPANSION': 'none',
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': True,
    'NATIVE_SCROLLBARS': True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'core.middlewares.middlewares.TokenAuthMiddleWare',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cid.middleware.CidMiddleware',
    'core.middlewares.middlewares.CustomLoggerMiddleware',
    'core.middlewares.middlewares.FixMalformedLimitParamMiddleware',
    'core.middlewares.middlewares.ResponseHeadersMiddleware',
    'core.middlewares.middlewares.CurrentUserMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '/core/common/templates/'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB', 'postgres'),
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_PASSWORD', 'Postgres123'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', 5432),
    }
}

ES_HOST = os.environ.get('ES_HOST', 'es')
ES_PORT = os.environ.get('ES_PORT', '9200')
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': [ES_HOST + ':' + ES_PORT]
    },
}

ENV = os.environ.get('ENVIRONMENT', 'development')
CID_GENERATE = True
CID_RESPONSE_HEADER = None
if ENV and ENV not in ['ci', 'development']:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[cid: %(cid)s] %(levelname)s %(asctime)s %(message)s'
            },
            'simple': {
                'format': '[cid: %(cid)s] %(asctime)s %(message)s'
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'correlation': {
                '()': 'cid.log.CidContextFilter'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'filters': ['require_debug_true', 'correlation'],
                'formatter': 'simple',
            },
            'request_handler': {
                'filters': ['require_debug_false', 'correlation'],
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['console', 'request_handler'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'core.users.password_validation.AlphaNumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
TIME_ZONE_PLACE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = '/staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

AUTH_USER_MODEL = 'users.UserProfile'
TEST_RUNNER = 'core.common.tests.CustomTestRunner'
DEFAULT_LOCALE = os.environ.get('DEFAULT_LOCALE', 'en')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'oclapi2-dev')
AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME', 'us-east-2')
DISABLE_VALIDATION = os.environ.get('DISABLE_VALIDATION', False)
API_SUPERUSER_PASSWORD = os.environ.get('API_SUPERUSER_PASSWORD', 'Root123')  # password for ocladmin superuser
API_SUPERUSER_TOKEN = os.environ.get('API_SUPERUSER_TOKEN', '891b4b17feab99f3ff7e5b5d04ccc5da7aa96da6')

# Redis
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_DB = 0
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

# django cache
if ENV and ENV not in ['ci']:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
        }
    }

# Celery
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "UTC"
CELERY_ALWAYS_EAGER = False
CELERY_WORKER_DISABLE_RATE_LIMITS = False
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # Reserve one task at a time
CELERY_TASK_ACKS_LATE = True  # Retry task in case of failure
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
)
CELERY_TASK_IGNORE_RESULT = False
CELERY_TASK_PUBLISH_RETRY = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_ROUTES = {
    'core.common.tasks.handle_save': {'queue': 'indexing'},
    'core.common.tasks.handle_m2m_changed': {'queue': 'indexing'},
    'core.common.tasks.handle_pre_delete': {'queue': 'indexing'},
    'core.common.tasks.populate_indexes': {'queue': 'indexing'},
    'core.common.tasks.rebuild_indexes': {'queue': 'indexing'}
}
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {
    'retry_policy': {
        'timeout': 10.0
    }
}
CELERY_RESULT_EXPIRES = 259200  # 72 hours
CELERY_BROKER_URL = CELERY_RESULT_BACKEND
CELERY_BROKER_POOL_LIMIT = 50  # should be adjusted considering the number of threads
CELERY_BROKER_CONNECTION_TIMEOUT = 10.0
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 259200}  # 72 hours, the lon
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': CELERY_RESULT_BACKEND,
    }
}
ELASTICSEARCH_DSL_PARALLEL = True
ELASTICSEARCH_DSL_AUTO_REFRESH = True
ELASTICSEARCH_DSL_AUTOSYNC = True
ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = 'core.common.models.CelerySignalProcessor'
ES_SYNC = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Only used for flower
FLOWER_USER = os.environ.get('FLOWER_USER', 'root')
FLOWER_PASSWORD = os.environ.get('FLOWER_PASSWORD', 'Root123')
FLOWER_HOST = os.environ.get('FLOWER_HOST', 'flower')
FLOWER_PORT = os.environ.get('FLOWER_PORT', 5555)
DATA_UPLOAD_MAX_MEMORY_SIZE = 200*1024*1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 200*1024*1024

# Mail settings
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True) in ['true', True]
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'no-reply@openconceptlab.org')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
COMMUNITY_EMAIL = os.environ.get('COMMUNITY_EMAIL', 'community@openconceptlab.org')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'openconceptlab <noreply@openconceptlab.org>')
ACCOUNT_EMAIL_SUBJECT_PREFIX = os.environ.get('ACCOUNT_EMAIL_SUBJECT_PREFIX', '[openconceptlab.org] ')
ADMINS = (
    ('Jonathan Payne', 'paynejd@gmail.com'),
)

if ENV and ENV != 'development':
    # Serving swagger static files (inserted after SecurityMiddleware)
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

if not ENV or ENV in ['production']:
    EMAIL_SUBJECT_PREFIX = '[Openconceptlab.org] '
else:
    EMAIL_SUBJECT_PREFIX = f'[Openconceptlab.org] [{ENV.upper()}]'

if not ENV or ENV in ['development', 'ci']:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

VERSION = __version__

# Errbit
ERRBIT_URL = os.environ.get('ERRBIT_URL', 'http://errbit:8080')
ERRBIT_KEY = os.environ.get('ERRBIT_KEY', 'errbit-key')

# Repo Export Upload/download
EXPORT_SERVICE = os.environ.get('EXPORT_SERVICE', 'core.common.services.S3')

# Locales Repository URI
# can either be /orgs/OCL/sources/Locales/ (old-style, ISO-639-2)
# or /orgs/ISO/sources/iso639-1/ (ISO-639-1, OCL's new default)
DEFAULT_LOCALES_REPO_URI = os.environ.get('DEFAULT_LOCALES_REPO_URI', '/orgs/ISO/sources/iso639-1/')

# keyCloak/OIDC Provider settings
OIDC_SERVER_URL = os.environ.get('OIDC_SERVER_URL', '')
OIDC_RP_CLIENT_ID = ''  # only needed a defined var in mozilla_django_oidc
OIDC_RP_CLIENT_SECRET = ''  # only needed a defined var in mozilla_django_oidc
OIDC_SERVER_INTERNAL_URL = os.environ.get('OIDC_SERVER_INTERNAL_URL', '') or OIDC_SERVER_URL
OIDC_REALM = os.environ.get('OIDC_REALM', 'ocl')
OIDC_OP_AUTHORIZATION_ENDPOINT = f'{OIDC_SERVER_URL}/realms/{OIDC_REALM}/protocol/openid-connect/auth'
OIDC_OP_LOGOUT_ENDPOINT = f'{OIDC_SERVER_URL}/realms/{OIDC_REALM}/protocol/openid-connect/logout'
OIDC_OP_TOKEN_ENDPOINT = f'{OIDC_SERVER_INTERNAL_URL}/realms/{OIDC_REALM}/protocol/openid-connect/token'
OIDC_OP_USER_ENDPOINT = f'{OIDC_SERVER_INTERNAL_URL}/realms/{OIDC_REALM}/protocol/openid-connect/userinfo'
OIDC_RP_SIGN_ALGO = 'RS256'
OIDC_OP_JWKS_ENDPOINT = f'{OIDC_SERVER_INTERNAL_URL}/realms/{OIDC_REALM}/protocol/openid-connect/certs'
OIDC_VERIFY_SSL = False
OIDC_VERIFY_JWT = True
OIDC_RP_SCOPES = 'openid profile email'
OIDC_STORE_ACCESS_TOKEN = True
OIDC_CREATE_USER = True
OIDC_CALLBACK_CLASS = 'core.users.views.OCLOIDCAuthenticationCallbackView'
