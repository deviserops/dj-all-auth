from . import views
from django.urls import path, include
from . import base_template as template_name
from .services.auth import views as auth_view
from django.contrib.auth import views as d_view

# connection service urls
from .services.connections.steam.urls import steam_urlpatterns
from .services.connections.google.urls import google_urlpatterns
from .services.connections.twitch.urls import twitch_urlpatterns
from .services.connections.discord.urls import discord_urlpatterns

# account service urls
from .services.profile.urls import profile_urlpatterns
from .services.security.urls import security_urlpatterns

d_view.LoginView.template_name = template_name + '/auth/login.html'
d_view.LogoutView.template_name = template_name + '/auth/logout.html'
# TODO Add password change layout in panel
# d_view.PasswordChangeView.template_name = template_name + '/auth/login.html'
# d_view.PasswordChangeDoneView.template_name = template_name + '/auth/login.html'
d_view.PasswordResetView.template_name = template_name + '/auth/password_reset.html'
d_view.PasswordResetDoneView.template_name = template_name + '/auth/password_reset_done.html'
d_view.PasswordResetConfirmView.template_name = template_name + '/auth/password_reset_confirm.html'
d_view.PasswordResetCompleteView.template_name = template_name + '/auth/password_reset_complete.html'

urlpatterns = [
    path('', include("django.contrib.auth.urls")),  # auth urls
    path('', views.Index.as_view(), name='__account'),  # base account page dashboard

    # Auth service
    path('register/', auth_view.Register.as_view(), name='__account_register'),
    path('request-account-activation/', auth_view.ActivateRequest.as_view(), name='__activate_request'),
    path('account-activate/<uidb64>/<token>', auth_view.ActivateAccount.as_view(), name='__activate_account'),

    # connection services
    path('steam/', include(steam_urlpatterns)),
    path('twitch/', include(twitch_urlpatterns)),
    path('google/', include(google_urlpatterns)),
    path('discord/', include(discord_urlpatterns)),

    # account service
    path('profile/', include(profile_urlpatterns)),
    path('security/', include(security_urlpatterns))
]
