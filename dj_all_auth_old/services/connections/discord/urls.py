from . import views
from django.urls import path

discord_urlpatterns = [
    path('authenticate', views.Authenticate.as_view(), name='__account_discord_authenticate'),
    path('authenticated', views.Authenticated.as_view(), name='__account_discord_authenticated'),
    path('revoke-authenticate', views.UnAuthenticate.as_view(), name='__account_discord_unauthenticate')
]
