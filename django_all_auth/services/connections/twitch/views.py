import logging
from .Twitch import Twitch
from .... import REDIRECT_URI_NAME
from django.shortcuts import redirect
from django.views.generic import View
from .models import Twitch as TwitchModel
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(decorator=login_required, name='dispatch')
class Authenticate(View):
    def get(self, request):
        twitch = Twitch()
        return_url = twitch.build_url(request, '__account_twitch_authenticated')
        twitch_login_url = twitch.auth_url(request, return_url)
        return redirect(twitch_login_url)


@method_decorator(decorator=login_required, name='dispatch')
class Authenticated(View):

    def get(self, request):
        twitch = Twitch()
        redirect_url = twitch.build_url(request, '__account_twitch_authenticated')
        payload = twitch.verify_auth(request, redirect_url)
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
                TwitchModel.objects.update_or_create(user=request.user, defaults=data)
        except Exception as e:
            logging.error(str(e))


@method_decorator(decorator=login_required, name='dispatch')
class UnAuthenticate(View):
    def get(self, request):
        twitch = Twitch()
        twitch.revoke_token(request.user)
        return redirect(REDIRECT_URI_NAME)
