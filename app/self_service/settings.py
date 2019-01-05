import ldap
import os
from distutils.util import strtobool
from django_auth_ldap.config import LDAPSearch
from django_auth_ldap.config import NestedActiveDirectoryGroupType

ROOT_URLCONF = 'self_service.urls'
WSGI_APPLICATION = 'self_service.wsgi.application'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ['DJANGO_DATA_DIR']

LOGIN_URL = '/login/'
STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
TEMPLATES_DIRS = [os.path.join(BASE_DIR, 'templates')]

SESSION_COOKIE_AGE = int(os.getenv('DJANGO_SESSION', 1209600))
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED', '*').strip('"').split(' ')
DEBUG = strtobool(os.getenv('DJANGO_DEBUG', 'True'))
SECRET_KEY = os.getenv('DJANGO_SECRET', 'localhost')
STATIC_ROOT = os.environ['DJANGO_STATIC_DIR']

DATETIME_FORMAT = os.getenv('DATETIME_FORMAT', 'N j, Y, f A').strip('"')
TIME_ZONE = os.getenv('TZ', 'America/Los_Angeles')
LANGUAGE_CODE = 'en-us'

USE_I18N = True
USE_L10N = False
USE_TZ = True

if DEBUG:
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    def show_toolbar(request):
        return True if request.user.is_staff else False

    DEBUG_TOOLBAR_CONFIG = {'SHOW_TOOLBAR_CALLBACK': show_toolbar}

if 'DJANGO_DEV_DB' in os.environ:
    if os.environ['DJANGO_DEV_DB'].startswith('/'):
        db_file = os.environ['DJANGO_DEV_DB']
    else:
        db_file = os.path.join(DATA_DIR, os.environ['DJANGO_DEV_DB'])
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_file,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['DATABASE_NAME'],
            'USER': os.environ['DATABASE_USER'],
            'PASSWORD': os.environ['DATABASE_PASS'],
            'HOST': os.environ['DATABASE_HOST'],
            'PORT': os.environ['DATABASE_PORT'],
            'OPTIONS': {
                'isolation_level': 'repeatable read',
                'init_command': "SET sql_mode='STRICT_ALL_TABLES'",
            },
        }
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - %(filename)s %(module)s.%(funcName)s:%(lineno)d - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'app': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_APP_LOG_LEVEL', 'DEBUG'),
            'propagate': True,
        },
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'debug_toolbar',
    'home',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATES_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# https://github.com/almet/django-auth-ldap/blob/master/docs/index.rst

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 1,
    ldap.OPT_REFERRALS: 0,
}

AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_ALLOW: 1,
    ldap.OPT_X_TLS_REQUIRE_CERT: 0,
}

AUTH_LDAP_BIND_DN = os.environ['LDAP_USER']
AUTH_LDAP_BIND_PASSWORD = os.environ['LDAP_PASS']
AUTH_LDAP_SERVER_URI = os.environ['LDAP_HOST']

AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType()
AUTH_LDAP_USER_SEARCH = LDAPSearch('dc=bigfish,dc=lan', ldap.SCOPE_SUBTREE, '(sAMAccountName=%(user)s)')
AUTH_LDAP_GROUP_SEARCH = LDAPSearch('DC=bigfish,DC=lan', ldap.SCOPE_SUBTREE, '(objectClass=group)')

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    'is_staff': os.environ['LDAP_STAFF_CN'].strip('"'),
    'is_superuser': os.environ['LDAP_SUPER_CN'].strip('"'),
}

AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'username': 'sAMAccountName',
    'email': 'mail',
}

AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_MIRROR_GROUPS = True
