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
from .models import Twitch as TwitchModel
from django.utils.translation import gettext as _
from django.utils.translation import get_language
from django.http.response import HttpResponseForbidden
from django.contrib.sites.shortcuts import get_current_site


class Twitch:
    def __init__(self):
        config = settings.DJ_ALL_AUTH.get('CONNECTIONS').get('TWITCH', None) if settings.DJ_ALL_AUTH.get(
            'CONNECTIONS') else settings.DJ_ALL_AUTH.get('CONNECTIONS')

        self.client_id = config.get('CLIENT_ID', None) if config else None
        self.client_secret = config.get('CLIENT_SECRET', None) if config else None

        # set scopes
        self.default_scope = ['openid', 'user:read:email']
        self.scope = config.get('SCOPE', self.default_scope) if config else self.default_scope
        self.update_scope()

        self.authentication_url = f'https://id.twitch.tv/oauth2/authorize'
        self.oauth2_host = 'id.twitch.tv'
        self.oauth2_token = '/oauth2/token'
        self.oauth2_validate = '/oauth2/validate'
        self.oauth2_revoke = '/oauth2/revoke'
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
            "force_verify": True,
            "response_type": 'code',
            "client_secret": self.client_secret,
            "client_id": self.client_id,
            "scope": f'{" ".join(self.scope)}',
            "nonce": nonce,
            "state": state
        }
        encoded_param = urlencode(auth_param)
        claims = {"id_token": {"email": None, "nonce": None, "email_verified": None}, "userinfo": {"picture": None}}
        return f'{self.authentication_url}?{encoded_param}&redirect_uri={redirect_url}&claims={json.dumps(claims)}'

    def verify_auth(self, request, redirect_url):
        response = {}
        try:
            state = request.GET.get('state', None)
            if request.session.get('state') != state:
                logging.error('Invalid access')
                return {}

            payload = {
                'client_id': self.client_id,
                'code': request.GET.get('code', None),
                'client_secret': self.client_secret,
                'redirect_uri': redirect_url,
                'grant_type': 'authorization_code',
            }
            headers = {
                'Content-Type': 'application/json'
            }
            response = self.call_api(self.oauth2_host, self.oauth2_token, 'POST', payload=payload, headers=headers)
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
        iss_list = ['https://id.twitch.tv/oauth2', 'id.twitch.tv/oauth2']
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
        connection = TwitchModel.objects.filter(user=user).first()
        if connection:
            payload = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': connection.refresh_token,
                'grant_type': 'refresh_token',
            }
            headers = {
                'Content-Type': 'application/json'
            }
            response = self.call_api(self.oauth2_host, self.oauth2_token, 'POST', payload=payload, headers=headers)
            access_token = response.get('access_token', None)
            refresh_token = response.get('refresh_token', None)
            if response is None or access_token is None or refresh_token is None:
                return HttpResponseForbidden(_('invalid_access'))

            connection.access_token = response.get('access_token')
            connection.refresh_token = response.get('refresh_token')
            connection.expires_in = response.get('expires_in')
            connection.token_type = response.get('token_type')
            connection.save()

    def validate_token(self, user):
        result = False
        connection = TwitchModel.objects.filter(user=user).first()
        if connection:
            headers = {
                'Authorization': f'Bearer {connection.access_token}'
            }
            response = self.call_api(self.oauth2_host, self.oauth2_validate, 'GET', None, headers)
            if response.get('client_id', None) == self.client_id:
                result = True
        return result

    def revoke_token(self, user):
        self.refresh_token(user)

        connection = TwitchModel.objects.filter(user=user).first()
        if connection:
            payload = {
                'client_id': self.client_id,
                'token': f'{connection.access_token}'
            }
            payload = urlencode(payload)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            self.call_api(self.oauth2_host, self.oauth2_revoke, 'POST', payload, headers)
            connection.delete()

    def call_api(self, host, end_point, method='GET', payload=None, headers=None):
        if headers is None:
            headers = {}

        if payload is not None and not isinstance(payload, str):
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
