import os, sys
import environ

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_ID         = env.int("SITE_ID", default=1)
DEBUG           = env.bool("DEBUG", default=False)
SECRET_KEY      = env.str("SECRET_KEY")
DOMAIN          = env.str("DOMAIN")
ALLOWED_HOSTS   = env.list("ALLOWED_HOSTS", default=[])

DEFAULT_AUTO_FIELD  = 'django.db.models.AutoField'
WSGI_APPLICATION    = 'config.wsgi.application'
LANGUAGE_CODE       = 'en-us'
USE_TZ              = True
TIME_ZONE           = 'UTC'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # external apps
    'corsheaders',
    'django_celery_results',
    'django_celery_beat',
    'django_extensions',
    # internal apps
    'apps.core',
    'apps.llm_test',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

DATABASES = {
    'default': {
        'ENGINE'    : env.str('DB_ENGINE', 'django.db.backends.postgresql'),
        'HOST'      : env.str('DB_HOST'),
        'PORT'      : env.int('DB_PORT', 5432),
        'NAME'      : env.str('DB_NAME'),
        'USER'      : env.str('DB_USER'),
        'PASSWORD'  : env.str('DB_PASSWORD'),
    }
}

# -- Celery settings ----------------------------------------------------------
CELERY_BROKER_URL           = env.str('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND       = 'django-db'
CELERY_RESULT_EXTENDED      = True
CELERY_TASK_TRACK_STARTED   = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # collectstatic will put files here
STORAGES = {
    # "default": {
    #     "BACKEND": "django_minio_backend.models.MinioBackend",
    # },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}

# DEBUG
DEBUG_TOOLBAR = env.bool('DEBUG_TOOLBAR', False)
if DEBUG_TOOLBAR:
    # import socket
    # hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    # INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

    INSTALLED_APPS = INSTALLED_APPS + [
        "debug_toolbar",
        # "django.contrib.staticfiles",
    ]
    MIDDLEWARE = MIDDLEWARE + [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG
    }

# AUTH
AUTH_PASSWORD_VALIDATORS = [] if DEBUG else [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'django_password_validators.password_character_requirements.password_validation.PasswordCharacterValidator',
        'OPTIONS': {
             'min_length_digit': 1,
             'min_length_lower': 1,
             'min_length_upper': 1,
         }
    },
]

# EMAIL
EMAIL_BACKEND       = env.str('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST          = env.str('EMAIL_HOST'          , '')
EMAIL_PORT          = env.int('EMAIL_PORT'          , 587)
EMAIL_USE_TLS       = env.bool('EMAIL_USE_TLS'      , 'False')
EMAIL_HOST_USER     = env.str('EMAIL_HOST_USER'     , '')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD' , '')
# Default email address to use for various automated correspondence from the site manager(s).
# This doesn't include error messages sent to ADMINS and MANAGERS;
# for that, see SERVER_EMAIL.
DEFAULT_FROM_EMAIL      = env.str('DEFAULT_FROM_EMAIL')
# DEFAULT_REPLY_TO_EMAIL  = list(filter(None, os.environ.get('DEFAULT_REPLY_TO_EMAIL', '').split(' ')))
DEFAULT_REPLY_TO_EMAIL  = env.str('DEFAULT_REPLY_TO_EMAIL', '')
# The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
SERVER_EMAIL        = env.str('SERVER_EMAIL')
# A list of all the people who get code error notifications (when DEBUG=False)
# ADMINS              = env.tuple('ADMINS', [('Admin', 'test@test.com'), ])
# A list in the same format as ADMINS that specifies who should get broken link notifications
# when BrokenLinkEmailsMiddleware is enabled.
# MANAGERS            = env.tuple('MANAGERS', ['Manager', 'manager@test.com'])


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'main': {
            'handlers': ['console'],
            'level': os.getenv('LOGGER_MAIN_LEVEL', 'WARNING'),
        },
    },
}
