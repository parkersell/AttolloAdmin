from attollo.settings.common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['104.236.231.193', 'localhost']

# Digital Ocean PostGresql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test1',
        'USER': 'devpsu',
        'PASSWORD': 'psu',
        'HOST': 'localhost',
        'PORT': '',
    }
}