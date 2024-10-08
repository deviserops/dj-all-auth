import re
import logging
import http.client
from urllib.parse import urlencode
from django.shortcuts import reverse
from .models import Steam as SteamModel
from django.utils.translation import get_language
from django.contrib.sites.shortcuts import get_current_site


class Steam:
    def get_domain(self, request):
        current_site = get_current_site(request)
        return f'{request.scheme}://{current_site}'

    def build_url(self, request, name):
        domain = self.get_domain(request)
        redirect_endpoint = reverse(name)
        if get_language():
            redirect_endpoint = redirect_endpoint.replace(f'/{get_language()}', '', 1)
        return f'{domain}{redirect_endpoint}'

    def login_url(self, request, return_url):
        domain = self.get_domain(request)
        login_url_params = {
            'openid.ns': 'http://specs.openid.net/auth/2.0',
            'openid.mode': 'checkid_setup',
            'openid.return_to': return_url,
            'openid.realm': domain,
            'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
            'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
        }
        encoded_param = urlencode(login_url_params)
        steam_login_url = f'https://steamcommunity.com/openid/login?{encoded_param}'
        return steam_login_url

    def verify_login(self, request):
        response = {}
        try:
            open_id_param = {
                'openid.assoc_handle': request.GET.get('openid.assoc_handle', None),
                'openid.signed': request.GET.get('openid.signed', None),
                'openid.sig': request.GET.get('openid.sig', None),
                'openid.ns': request.GET.get('openid.ns', None),
                'openid.op_endpoint': request.GET.get('openid.op_endpoint', None),
                'openid.claimed_id': request.GET.get('openid.claimed_id', None),
                'openid.identity': request.GET.get('openid.identity', None),
                'openid.return_to': request.GET.get('openid.return_to', None),
                'openid.response_nonce': request.GET.get('openid.response_nonce', None),
                'openid.mode': 'check_authentication',
            }
            payload = urlencode(open_id_param)
            headers = {
                'Accept-language': ' en',
                'Content-type': 'application/x-www-form-urlencoded'
            }

            # verify login
            conn = http.client.HTTPSConnection('steamcommunity.com')
            conn.request('POST', '/openid/login', payload, headers)
            res = conn.getresponse()
            data = res.read()
            result = data.decode("utf-8")
            if re.search(r"is_valid\s*:\s*true", result, re.IGNORECASE):
                match = re.match(r"^https://steamcommunity.com/openid/id/(\d{17,50})",
                                 request.GET.get('openid.claimed_id'))
                steamid = match.group(1)  # Extract the Steam ID from the match object
                response.update({'steamid': steamid})
        except Exception as e:
            logging.error(str(e))
        return response

    def revoke(self, user):
        connection = SteamModel.objects.filter(user=user).first()
        if connection:
            connection.delete()
