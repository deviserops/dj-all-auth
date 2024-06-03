import logging
from .Discord import Discord
from .... import REDIRECT_URI_NAME
from django.shortcuts import redirect
from django.views.generic import View
from .models import Discord as DiscordModel
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(decorator=login_required, name='dispatch')
class Authenticate(View):
    def get(self, request):
        discord = Discord()
        return_url = discord.build_url(request, '__account_discord_authenticated')
        discord_login_url = discord.auth_url(request, return_url)
        return redirect(discord_login_url)


@method_decorator(decorator=login_required, name='dispatch')
class Authenticated(View):

    def get(self, request):
        discord = Discord()
        redirect_url = discord.build_url(request, '__account_discord_authenticated')
        payload = discord.verify_auth(request, redirect_url)
        self.save_connection(request, payload)
        return redirect(REDIRECT_URI_NAME)

    def save_connection(self, request, payload):
        try:
            if payload.get('access_token') and payload.get('refresh_token'):
                data = {
                    'user': request.user,
                    'access_token': payload.get('access_token'),
                    'expires_in': payload.get('expires_in'),
                    'refresh_token': payload.get('refresh_token', None),
                    'token_type': payload.get('token_type')
                }
                DiscordModel.objects.update_or_create(user=request.user, defaults=data)
        except Exception as e:
            logging.error(str(e))


@method_decorator(decorator=login_required, name='dispatch')
class UnAuthenticate(View):
    def get(self, request):
        discord = Discord()
        discord.revoke_token(request.user)
        return redirect(REDIRECT_URI_NAME)
