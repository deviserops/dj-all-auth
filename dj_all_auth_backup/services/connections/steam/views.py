import logging
from .Steam import Steam
from .... import REDIRECT_URI_NAME
from django.views.generic import View
from django.shortcuts import redirect
from .models import Steam as SteamModel
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(decorator=login_required, name='dispatch')
class Authenticate(View):
    def get(self, request):
        steam = Steam()
        return_url = steam.build_url(request, '__account_steam_authenticated')
        steam_login_url = steam.login_url(request, return_url)
        return redirect(steam_login_url)


@method_decorator(decorator=login_required, name='dispatch')
class Authenticated(View):

    def get(self, request):
        steam = Steam()
        payload = steam.verify_login(request)
        self.save_connection(request, payload)
        return redirect(REDIRECT_URI_NAME)

    def save_connection(self, request, payload):
        try:
            if payload.get('steamid'):
                data = {
                    'user': request.user,
                    'steam_id': payload.get('steamid'),
                }
                SteamModel.objects.update_or_create(user=request.user, defaults=data)
        except Exception as e:
            logging.error(str(e))


@method_decorator(decorator=login_required, name='dispatch')
class UnAuthenticate(View):
    def get(self, request):
        steam = Steam()
        steam.revoke(request.user)
        return redirect(REDIRECT_URI_NAME)
