from .shared import(
    BASE_DIR,
    PROJ_DIR,
    SECRET_KEY,
    DEBUG,
    ALLOWED_HOSTS,
    INSTALLED_APPS,
    MIDDLEWARE,
    ROOT_URLCONF,
    TEMPLATES,
    WSGI_APPLICATION,
    DATABASES,
    AUTH_PASSWORD_VALIDATORS,
    LANGUAGE_CODE,
    TIME_ZONE,
    USE_I18N,
    USE_L10N,
    USE_TZ,
    STATIC_URL,
    STATICFILES_DIRS,
    STATIC_ROOT,
    MEDIA_ROOT,
    MEDIA_URL,
    APPEND_SLASH,
    LOGIN_URL,
    LOGIN_REDIRECT_URL,
    LOGOUT_REDIRECT_URL,
    AUTH_USER_MODEL,
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
    DEFAULT_FROM_EMAIL,
    REST_FRAMEWORK,
)

__all__ = [
    'BASE_DIR',
    'PROJ_DIR',
    'SECRET_KEY',
    'DEBUG',
    'ALLOWED_HOSTS',
    'INSTALLED_APPS',
    'MIDDLEWARE',
    'ROOT_URLCONF',
    'TEMPLATES',
    'WSGI_APPLICATION',
    'DATABASES',
    'AUTH_PASSWORD_VALIDATORS',
    'LANGUAGE_CODE',
    'TIME_ZONE',
    'USE_I18N',
    'USE_L10N',
    'USE_TZ',
    'STATIC_URL',
    'STATICFILES_DIRS',
    'STATIC_ROOT',
    'APPEND_SLASH',
    'INTERNAL_IPS',
    'LOGIN_URL',
    'LOGIN_REDIRECT_URL',
    'LOGOUT_REDIRECT_URL',
    'AUTH_USER_MODEL',
    'CELERY_BROKER_URL',
    'CELERY_RESULT_BACKEND',
    'DEFAULT_FROM_EMAIL',
    'REST_FRAMEWORK',
]
import sys 
sys.modules['fontawesome_free'] = __import__('fontawesome-free')

# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

DEBUG = True
INTERNAL_IPS = ['127.0.0.1', 'localhost']
INSTALLED_APPS = ['whitenoise.runserver_nostatic', 'fontawesome_free', "django_static_ionicons", *INSTALLED_APPS] # , 'debug_toolbar']

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'noreply@remy.network'
EMAIL_HOST_PASSWORD = 'axnqjwqztjxzjygs'
EMAIL_USE_TLS = True
