from django.urls import path, include

# connection service urls
from .services.connections.steam.urls import steam_urlpatterns
from .services.connections.google.urls import google_urlpatterns
from .services.connections.twitch.urls import twitch_urlpatterns
from .services.connections.discord.urls import discord_urlpatterns

urlpatterns = [
    # connection services
    path('steam/', include(steam_urlpatterns)),
    path('twitch/', include(twitch_urlpatterns)),
    path('google/', include(google_urlpatterns)),
    path('discord/', include(discord_urlpatterns)),
]
