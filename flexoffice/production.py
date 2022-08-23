import os
from django.conf import settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'daik63f62eelei',
        'USER': 'wpotnucugvnqed',
        'PASSWORD': '610fc42fe42c59cf14a896ad782099cd42c74cc8f586108fa3012f32e7ae63bb',
        'HOST': 'ec2-54-235-89-123.compute-1.amazonaws.com',
        'PORT': '5432',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'd4nq4v3023sdvc',
    #     'USER': 'ubbolfyuchbowt',
    #     'PASSWORD': '29614bea7abd6979e524710658080716898399098884965fafab4f4de9792b90',
    #     'HOST': 'ec2-23-21-94-99.compute-1.amazonaws.com',
    #     'PORT': '5432',
    # }
}
HOST = 'https://flexsoffice.herokuapp.com'
# HOST = 'https://snakescriptflexoffice.herokuapp.com'

STATIC_ROOT = os.path.join(settings.BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(settings.BASE_DIR , 'static')]


MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media')
MEDIA_URL = '/media/'

DEBUG = True
