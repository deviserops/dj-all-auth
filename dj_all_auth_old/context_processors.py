from . import __ac_logo, __ac_layout, __ac_app_name
from django.contrib.sites.shortcuts import get_current_site


def __config(request):
    config = {
        'ac_logo': __ac_logo,  # <- static path
        'ac_layout': __ac_layout,
        'ac_app_name': __ac_app_name,
    }
    return config


def __default_context(request):
    current_site = get_current_site(request)
    domain = f'{request.scheme}://{current_site}'
    site_name = current_site.name
    context = {
        'domain': domain,
        'site_name': site_name
    }
    return context
