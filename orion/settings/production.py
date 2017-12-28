from .base import *

DEBUG = True

ALLOWED_HOSTS = ['bdk93.pythonanywhere.com']

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/home/bdk93/my.cnf',
        },
    }
}
