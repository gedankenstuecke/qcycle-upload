"""
Django settings for oh_data_uploader project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import dj_database_url
from env_tools import apply_env

apply_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'whopsthereshouldbeone')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.getenv('DEBUG', '').lower() == 'false' else True

# Infer if this is running on Heroku based on this being set.
HEROKUCONFIG_APP_NAME = os.getenv('HEROKUCONFIG_APP_NAME', '')
ON_HEROKU = bool(HEROKUCONFIG_APP_NAME)

ALLOWED_HOSTS = ['*']

# Read OH settings from .env/environment variables
OPENHUMANS_OH_BASE_URL = os.getenv('OPENHUMANS_OH_BASE_URL',
                                   'https://www.openhumans.org')
OPENHUMANS_CLIENT_ID = os.getenv('OH_CLIENT_ID')
OPENHUMANS_CLIENT_SECRET = os.getenv('OH_CLIENT_SECRET')

# Set up base URL.
DEFAULT_BASE_URL = ('https://{}.herokuapp.com'.format(HEROKUCONFIG_APP_NAME) if
                    ON_HEROKU else 'http://127.0.0.1:5000')
OPENHUMANS_APP_BASE_URL = os.getenv('APP_BASE_URL', DEFAULT_BASE_URL)
if OPENHUMANS_APP_BASE_URL[-1] == "/":
    OPENHUMANS_APP_BASE_URL = OPENHUMANS_APP_BASE_URL[:-1]

# Admin account password for configuration.
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.Main',
    'open_humans.apps.OpenHumansConfig',
    'project_admin.apps.ProjectAdminConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'main': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'oh_data_uploader': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'open_humans': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
}

ROOT_URLCONF = 'oh_data_uploader.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.read_config'
            ],
        },
    },
]

WSGI_APPLICATION = 'oh_data_uploader.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if ON_HEROKU:
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES = {'default': db_from_env}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
