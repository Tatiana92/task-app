"""
Django settings for task project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import os.path
import djcelery

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1i-flvrsw-%z4_8b7*4b)3x&w+@^3o7+^%cxs6b3(q%2t$qqut'

djcelery.setup_loader()

CELERYBEAT_SCHEDULER="djcelery.schedulers.DatabaseScheduler"
CELERY_ALWAYS_EAGER=False
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'clients',
    'djcelery',
    'djkombu',
)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'task.urls'

WSGI_APPLICATION = 'task.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

TASK_PATH = os.path.split( os.path.dirname(__file__).replace('\\', '/') )[0]
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = TASK_PATH + MEDIA_URL

STATICFILES_DIRS = []
STATICFILES_DIRS.extend([
    TASK_PATH + '/static',
])