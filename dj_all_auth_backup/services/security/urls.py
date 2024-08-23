from . import views
from django.urls import path

security_urlpatterns = [
    path('', views.Index.as_view(), name='__account_security_index'),
]
