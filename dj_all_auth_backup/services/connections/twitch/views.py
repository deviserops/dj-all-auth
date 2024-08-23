import random
import logging

from .Twitch import Twitch
from django.db import transaction
from .... import REDIRECT_URI_NAME
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import View
from .models import Twitch as TwitchModel
from django.utils.translation import gettext as _
from django.core.exceptions import FieldDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required


class Authenticate(View):
    def get(self, request):
        twitch = Twitch()
        return_url = twitch.build_url(request, '__account_twitch_authenticated')
        twitch_login_url = twitch.auth_url(request, return_url)
        return redirect(twitch_login_url)


class Authenticated(View):
    def get(self, request):
        twitch = Twitch()
        redirect_url = twitch.build_url(request, '__account_twitch_authenticated')
        payload = twitch.verify_auth(request, redirect_url)
        self.save_connection(request, payload)
        return redirect(REDIRECT_URI_NAME)

    @transaction.atomic
    def save_connection(self, request, payload):
        try:
            twitch = Twitch()
            identifier, email = twitch.validate_payload(payload)

            if not email:
                return False

            data = {
                'identifier': identifier,
                'id_token': payload.get('id_token'),
                'access_token': payload.get('access_token'),
                'expires_in': payload.get('expires_in'),
                'refresh_token': payload.get('refresh_token', None),
                'token_type': payload.get('token_type')
            }

            user = request.user if not request.user.is_anonymous else None

            if not user:
                is_exist = TwitchModel.objects.filter(email=email).first()
                if not is_exist:
                    payload = {
                        'username': self.clear_username(request, email.split('@')[0].split('+')[0])
                    }

                    # check if email is required
                    if self.is_field_unique(get_user_model(), 'email'):
                        payload.update({"email": email})
                        user = get_user_model().objects.filter(email=email).first()

                    user = get_user_model().objects.create_user(**payload) if not user else user
                    data.update({'user': user})
                else:
                    user = is_exist.user
                TwitchModel.objects.update_or_create(email=email, defaults=data)
                login(request, user)
            else:
                data.update({
                    'email': email,
                })
                is_another_account = TwitchModel.objects.filter(email=email).first()
                if is_another_account:
                    messages.error(self.request, _('account_with_this_connection_already_exist'))
                    return False
                TwitchModel.objects.update_or_create(user=user, defaults=data)
        except Exception as e:
            logging.error(str(e))

    def is_field_unique(self, model, field_name):
        try:
            field = model._meta.get_field(field_name)
            return field.unique
        except FieldDoesNotExist:
            return False

    def clear_username(self, request, username):
        sanitized_username = ''.join(char for char in username if char.isalnum())
        if not sanitized_username:
            return None
        is_exist = get_user_model().objects.filter(username=sanitized_username).first()
        if not is_exist:
            return sanitized_username
        updated_username = f'{sanitized_username}{random.randint(1, 9)}'
        return self.clear_username(request, updated_username)


@method_decorator(decorator=login_required, name='dispatch')
class UnAuthenticate(View):
    def get(self, request):
        if not request.user.email:
            messages.error(self.request, _('add_email_to_unlink_account'))
            return redirect(REDIRECT_URI_NAME)
        twitch = Twitch()
        twitch.revoke_token(request.user)
        return redirect(REDIRECT_URI_NAME)
