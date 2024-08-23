import os
import uuid
import json
import base64
import hashlib
import logging
import http.client
from django.conf import settings
from urllib.parse import urlencode
from django.shortcuts import reverse
from .models import Google as GoogleModel
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.http.response import HttpResponseForbidden
from django.contrib.sites.shortcuts import get_current_site


class Google:

    def __init__(self):
        config = settings.DJ_ALL_AUTH.get('CONNECTIONS').get('GOOGLE', None) if settings.DJ_ALL_AUTH.get(
            'CONNECTIONS') else None

        self.client_id = config.get('CLIENT_ID', None) if config else None
        self.client_secret = config.get('CLIENT_SECRET', None) if config else None

        # set scopes
        self.default_scope = ['openid', 'email']
        self.scope = config.get('SCOPE', self.default_scope) if config else self.default_scope
        self.update_scope()

        self.authentication_url = f'https://accounts.google.com/o/oauth2/v2/auth'
        self.oauth2_host = 'oauth2.googleapis.com'
        self.oauth2_token = '/token'
        self.oauth2_revoke = '/revoke'
        self.api_status = None

    def update_scope(self):
        for scope in self.default_scope:
            if scope not in self.scope:
                self.scope.append(scope)

    def get_domain(self, request):
        current_site = get_current_site(request)
        return f'{request.scheme}://{current_site}'

    def build_url(self, request, name):
        domain = self.get_domain(request)
        redirect_endpoint = reverse(name)
        if get_language():
            redirect_endpoint = redirect_endpoint.replace(f'/{get_language()}', '', 1)
        return f'{domain}{redirect_endpoint}'

    def auth_url(self, request, redirect_url):
        # set session data
        state = hashlib.sha256(os.urandom(1024)).hexdigest()
        nonce = str(uuid.uuid4())
        request.session['state'] = state

        auth_param = {
            "prompt": 'consent',
            "response_type": 'code',
            "client_id": self.client_id,
            "scope": f'{" ".join(self.scope)}',
            "state": state,
            "login_hint": request.user.email if request.user and not request.user.is_anonymous else '',
            "nonce": nonce,
            "hd": self.get_domain(request),
            "access_type": 'offline'
        }
        encoded_param = urlencode(auth_param)
        return f'{self.authentication_url}?{encoded_param}&redirect_uri={redirect_url}'

    def verify_auth(self, request, redirect_url):
        response = {}
        try:
            state = request.GET.get('state', None)
            if request.session.get('state') != state:
                logging.error('Invalid access')
                return {}

            payload = {
                'code': request.GET.get('code', None),
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': redirect_url,
                'grant_type': 'authorization_code',
            }
            response = self.call_api(self.oauth2_host, self.oauth2_token, 'POST', payload=payload)
            access_token = response.get('access_token', None)
            refresh_token = response.get('refresh_token', None)
            if response is None or access_token is None or refresh_token is None:
                logging.error('Invalid access')
                return {}
        except Exception as e:
            logging.error(str(e))

        return response

    def validate_payload(self, connection):
        id_token = connection.get('id_token', None)
        if not id_token:
            return False

        header, payload, signature = id_token.split('.')
        payload = self.decode_base64(payload)
        payload = json.loads(payload)
        iss_list = ['https://accounts.google.com', 'accounts.google.com']
        identifier = payload.get('sub')

        if payload.get('iss', None) not in iss_list:
            return False

        if payload.get('aud') != self.client_id:
            return False

        # TODO add more validation

        return identifier, payload.get('email', False)

    def decode_base64(self, payload):
        """Decodes a base64 encoded string with proper padding handling."""
        missing_padding = len(payload) % 4
        if missing_padding != 0:
            payload += '=' * missing_padding

        return base64.b64decode(payload)

    def refresh_token(self, user):
        connection = GoogleModel.objects.filter(user=user).first()
        if connection:
            payload = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': connection.refresh_token,
                'grant_type': 'refresh_token',
            }
            response = self.call_api(self.oauth2_host, self.oauth2_token, 'POST', payload=payload)
            access_token = response.get('access_token', None)
            if response is None or access_token is None:
                return HttpResponseForbidden(_('invalid_access'))

            connection.access_token = response.get('access_token')
            connection.expires_in = response.get('expires_in')
            connection.token_type = response.get('token_type')
            connection.save()

    def revoke_token(self, user):
        connection = GoogleModel.objects.filter(user=user).first()
        if connection:
            payload = {
                'token': connection.access_token
            }
            self.call_api(self.oauth2_host, self.oauth2_revoke, 'POST', payload=payload)
            connection.delete()

    def call_api(self, host, end_point, method='GET', payload=None, headers=None):
        if headers is None:
            headers = {}

        if payload is not None:
            payload = json.dumps(payload)
        conn = http.client.HTTPSConnection(host)
        conn.request(method, end_point, payload, headers)
        res = conn.getresponse()
        self.api_status = res.status
        data = res.read()
        try:
            return json.loads(data.decode("utf-8"))
        except Exception as e:
            logging.error(str(e))
            return None
