from . import views
from django.urls import path

profile_urlpatterns = [
    path('', views.Index.as_view(), name='__account_profile_index'),
    path('profile-edit', views.ProfileEdit.as_view(), name='__account_profile_edit'),
    path('password-edit', views.PasswordEdit.as_view(), name='__account_password_edit'),
]
