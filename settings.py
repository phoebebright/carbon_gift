import sys, os
from datetime import date, datetime, timedelta
import pytz


ROOT = lambda base : os.path.abspath(os.path.join(os.path.dirname(__file__), base).replace('\\','/'))


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

REGISTRATION_OPEN = True

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, ROOT('libs'))
sys.path.insert(0, ROOT('tastypie'))
#sys.path.insert(0, os.getcwd())

BETA = True

DEBUG = True
TEMPLATE_DEBUG = DEBUG


ALLOWED_HOSTS = ['127.0.0.1','greenmyday.com','www.greenmyday.com', 'footprint.trialflight.com']


INTERNAL_IPS = ('217.115.117.19',)

SITE_URL = "http://footprint.trialflight.com"
HOSTNAME = "http://footprint.trialflight.com"

ADMINS = (
     ('Phoebe', 'phoebebright310+admin@gmail.com'),
)

NEW_USER_EMAILS = ('phoebebright310+admin@gmail.com',)
MANAGERS = ADMINS



EMAIL_HOST = "mail.beautifuldata.ie"
EMAIL_PORT = "25"
EMAIL_HOST_USER = "test@beautifuldata.ie"
EMAIL_HOST_PASSWORD = "cabbage123"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'footprints',

        'USER': 'footprints',
        'PASSWORD': 'cabbage',

    }
}
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

LANGUAGE_CODE = 'en-gb'

SITE_ID = 1


USE_I18N = True
USE_TZ = True


# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'shared_static')
STATIC_URL = '/shared_static/'


# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'theme/static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)



# Make this unique, and don't share it with anybody.
SECRET_KEY = 'xz9$kxtorhbnu^u7kg^-wt9_9ptw3*)jp2o!f0l*d-y9!!a$i('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    'django.core.context_processors.i18n',
    "django.core.context_processors.media",
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',



)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'carbongift.wsgi.application'
#WSGI_APPLICATION = None

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
    os.path.join(os.path.dirname(__file__), "templates/registration"),
    # os.path.join(os.path.dirname(__file__), "templates/mobile"),


    )
FIXTURE_DIRS = (
    ( "web/fixtures"),

)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'theme',  # just to hold static files for templates
    'django_tables2',
    'taggit',
    'web',
)

AUTH_USER_MODEL = 'web.MyUser'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/logout/'



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


try:
    from settings_local import *
except ImportError:
    pass