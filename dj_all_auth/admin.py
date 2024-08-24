from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from .models import Google, Steam, Twitch, Discord, EmailTemplate


class CustomUserModel(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(CustomUserModel, self).get_fieldsets(request, obj)
        if not request.user.is_superuser and obj:
            fieldsets = (
                (None, {"fields": ("username", "password")}),
                (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
                (_("Activation"), {"fields": ("is_active",), },),
                (_("Important dates"), {"fields": ("last_login", "date_joined")}),
            )
        return fieldsets

    # list only staff user
    def get_queryset(self, request):
        if request.user.is_superuser:
            return get_user_model().objects.filter()
        else:
            return get_user_model().objects.filter(is_superuser=False)


class EmailTemplateAdmin(admin.ModelAdmin):
    search_fields = ('template',)
    list_filter = ('template',)

    class Media:
        js = ['tinymce/tinymce.min.js', 'js/admin/django-admin-email-template.js']


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


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), CustomUserModel)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(Google, GoogleAdmin)
admin.site.register(Steam, SteamAdmin)
admin.site.register(Twitch, TwitchAdmin)
admin.site.register(Discord, DiscordAdmin)
