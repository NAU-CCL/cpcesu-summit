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
    LOGOUT_REDIRECT_URL,
    AUTH_USER_MODEL,
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
    'LOGIN_URL',
    'LOGOUT_REDIRECT_URL',
    'AUTH_USER_MODEL',
]

DEBUG = False
# SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = ['*']
LOGGING = {
    #  ... omitting the formatters and handlers for brevity ...
    'loggers': {
        # ...  you may have other loggers here as well ...
        'django': {
            'level': 'WARNING',
            'propagate': True,
        }
    }
}
