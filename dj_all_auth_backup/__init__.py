from django.conf import settings
from .apps import DjAllAuthConfig

config = DjAllAuthConfig
base_template = config.name

__ac_app_name = base_template
__ac_logo = settings.DJ_ALL_AUTH.get('LOGO') if settings.DJ_ALL_AUTH.get('LOGO') else f'{__ac_app_name}/images/logo.webp'
__ac_layout = f'{__ac_app_name}/layouts/base.html'

REDIRECT_URI_NAME = '__account_profile_index'
if settings.DJ_ALL_AUTH.get('CONNECTIONS'):
    __connection = settings.DJ_ALL_AUTH.get('CONNECTIONS')
    if __connection.get('REDIRECT_URI_NAME') is not None:
        REDIRECT_URI_NAME = __connection.get('REDIRECT_URI_NAME')
