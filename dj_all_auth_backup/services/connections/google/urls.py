from . import views
from django.urls import path

google_urlpatterns = [
    path('authenticate', views.Authenticate.as_view(), name='__account_google_authenticate'),
    path('authenticated', views.Authenticated.as_view(), name='__account_google_authenticated'),
    path('revoke-authenticate', views.UnAuthenticate.as_view(), name='__account_google_unauthenticate')
]
