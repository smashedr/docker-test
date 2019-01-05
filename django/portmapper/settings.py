import ldap
import os
from distutils.util import strtobool
from django_auth_ldap.config import LDAPSearch
from django_auth_ldap.config import NestedActiveDirectoryGroupType

ROOT_URLCONF = 'home.urls'
WSGI_APPLICATION = 'portmapper.wsgi.application'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ['DJANGO_DATA_DIR']

LOGIN_URL = '/login/'
STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
TEMPLATES_DIRS = [os.path.join(BASE_DIR, 'templates')]

SESSION_COOKIE_AGE = int(os.environ['DJANGO_SESSION'])
ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED'].split(' ')
DEBUG = strtobool(os.environ['DJANGO_DEBUG'])
SECRET_KEY = os.environ['DJANGO_SECRET']
STATIC_ROOT = os.environ['DJANGO_STATIC_DIR']

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/minute',
        'user': '180/minute'
    },
}

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
        }
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s %(module)s.%(funcName)s:%(lineno)d - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ['DJANGO_LOG_LEVEL'],
            'propagate': True,
        },
        'app': {
            'handlers': ['console'],
            'level': os.environ['DJANGO_APP_LOG_LEVEL'],
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
    'rest_framework',
    'home',
    'api',
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
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    'dc=bigfish,dc=lan',
    ldap.SCOPE_SUBTREE,
    '(sAMAccountName=%(user)s)',
)
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    'DC=bigfish,DC=lan',
    ldap.SCOPE_SUBTREE,
    '(objectClass=group)',
)

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
