from django.contrib import admin
from .models import Google, Steam, Twitch, Discord


class DefaultPermission(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class GoogleAdmin(DefaultPermission):
    search_fields = ('user__username', 'token_type', 'access_token', 'expires_in', 'date')
    list_filter = ('token_type',)
    list_display = ('user', 'token_type', 'access_token', 'expires_in', 'date')


class SteamAdmin(DefaultPermission):
    search_fields = ('user__username', 'steam_id', 'date')
    list_display = ('user', 'steam_id', 'date')


class TwitchAdmin(DefaultPermission):
    search_fields = ('user__username', 'token_type', 'access_token', 'expires_in', 'date')
    list_filter = ('token_type',)
    list_display = ('user', 'token_type', 'access_token', 'expires_in', 'date')


class DiscordAdmin(DefaultPermission):
    search_fields = ('user__username', 'identifier', 'expires_in', 'date')
    list_filter = ('token_type',)
    list_display = ('user', 'identifier', 'expires_in', 'date')


admin.site.register(Google, GoogleAdmin)
admin.site.register(Steam, SteamAdmin)
admin.site.register(Twitch, TwitchAdmin)
admin.site.register(Discord, DiscordAdmin)
