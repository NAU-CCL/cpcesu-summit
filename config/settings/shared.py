"""
Django settings for summit project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROJ_DIR = os.path.join(BASE_DIR, 'summit')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u&f_a@de&t00=pdfqc6x6^nif^w-+1eb_cf_g03!^&ch&cavs9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    # Default apps, keep them
    # Do not touch
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Do not touch

    # Other Django-related libraries (3rd party)
    'django_celery_beat',
]

PROJ_APPS = [
    # Project-based apps
    # Order alphabetically, first loading the libs over apps
    'summit.libs',
    'summit.libs.auth',
    'summit.apps.core',
    'summit.apps.docs',
    'summit.apps.projects'
]

INSTALLED_APPS = PROJ_APPS + DJANGO_APPS


# Middleware definition

DJANGO_MIDDLEWARES = [
    # Default middleware, keep them
    # Do not touch
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Do not touch
]

PROJ_MIDDLEWARES = [
    # Project-based middleware
    # Order based on queue / priority
]

MIDDLEWARE = DJANGO_MIDDLEWARES + PROJ_MIDDLEWARES


# Routing, templating, and WSGI

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJ_DIR, 'libs/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'summit.libs.templates.context_processors.notification_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cpcesupm',
        'USER': 'cpcesu',
        'PASSWORD': 'HjMNGN4cJtQcg',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
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

# Media files (PDFs, Docx, Google Docs, etc.)

MEDIA_URL = '/data/'


# Custom Shared config
STATICFILES_DIRS = ['%s/static' % PROJ_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'data')
APPEND_SLASH = True
LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = None
AUTH_USER_MODEL = 'summit_auth.User'


# TO DO STILL
# EMAIL_BACKEND =
# ADMINS
CELERY_BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'redis'
