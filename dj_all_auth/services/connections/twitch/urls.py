from . import views
from django.urls import path

twitch_urlpatterns = [
    path('authenticate', views.Authenticate.as_view(), name='__account_twitch_authenticate'),
    path('authenticated', views.Authenticated.as_view(), name='__account_twitch_authenticated'),
    path('revoke-authenticate', views.UnAuthenticate.as_view(), name='__account_twitch_unauthenticate')
]
