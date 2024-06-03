from . import views
from django.urls import path

steam_urlpatterns = [
    path('authenticate', views.Authenticate.as_view(), name='__account_steam_authenticate'),
    path('authenticated', views.Authenticated.as_view(), name='__account_steam_authenticated'),
    path('revoke-authenticate', views.UnAuthenticate.as_view(), name='__account_steam_unauthenticate')
]
