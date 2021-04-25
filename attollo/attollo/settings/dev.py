from attollo.settings.common import *

SECRET_KEY = 'm_i92jxyijfclsq^9#ko9)=#oy9(&yqifznt)-i4!&d)1!#r+4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['104.236.231.193', 'localhost']


# # Default Database
# # https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

GOOGLE_API_KEY = 'AIzaSyBAdEM87HNJTCIw1ryMBYyoks5O7tMTrF0'