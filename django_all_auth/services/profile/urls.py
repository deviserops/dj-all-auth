from . import views
from django.urls import path

profile_urlpatterns = [
    path('', views.Index.as_view(), name='__account_profile_index'),
    path('profile-edit', views.Edit.as_view(), name='__account_profile_edit'),
]
