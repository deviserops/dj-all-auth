from django.conf import settings
from .apps import DjAllAuthConfig

config = DjAllAuthConfig
base_template = config.name

REDIRECT_URI_NAME = '/'
if settings.DJ_ALL_AUTH.get('CONNECTIONS'):
    __connection = settings.DJ_ALL_AUTH.get('CONNECTIONS')
    if __connection.get('REDIRECT_URI_NAME') is not None:
        REDIRECT_URI_NAME = __connection.get('REDIRECT_URI_NAME')
