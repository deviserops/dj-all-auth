import logging
from .Google import Google
from .... import REDIRECT_URI_NAME
from django.views.generic import View
from django.shortcuts import redirect
from .models import Google as GoogleModel
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(decorator=login_required, name='dispatch')
class Authenticate(View):
    def get(self, request):
        google = Google()
        redirect_url = google.build_url(request, '__account_google_authenticated')
        authentication_url = google.auth_url(request, redirect_url)
        return redirect(authentication_url)


@method_decorator(decorator=login_required, name='dispatch')
class Authenticated(View):
    def get(self, request):
        google = Google()
        redirect_url = google.build_url(request, '__account_google_authenticated')
        payload = google.verify_auth(request, redirect_url)
        self.save_connection(self.request, payload)
        return redirect(REDIRECT_URI_NAME)

    def save_connection(self, request, payload):
        try:
            if payload.get('id_token'):
                data = {
                    'user': request.user,
                    'id_token': payload.get('id_token'),
                    'access_token': payload.get('access_token'),
                    'expires_in': payload.get('expires_in'),
                    'refresh_token': payload.get('refresh_token', None),
                    'token_type': payload.get('token_type')
                }
                GoogleModel.objects.update_or_create(user=request.user, defaults=data)
        except Exception as e:
            logging.error(str(e))


@method_decorator(decorator=login_required, name='dispatch')
class UnAuthenticate(View):
    def get(self, request):
        google = Google()
        google.revoke_token(request.user)
        return redirect(REDIRECT_URI_NAME)
