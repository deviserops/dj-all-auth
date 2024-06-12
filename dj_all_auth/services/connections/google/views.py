import random
import logging

from .Google import Google
from django.db import transaction
from .... import REDIRECT_URI_NAME
from django.contrib import messages
from django.views.generic import View
from django.shortcuts import redirect
from .models import Google as GoogleModel
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required


class Authenticate(View):
    def get(self, request):
        google = Google()
        redirect_url = google.build_url(request, '__account_google_authenticated')
        authentication_url = google.auth_url(request, redirect_url)
        return redirect(authentication_url)


class Authenticated(View):
    def get(self, request):
        google = Google()
        redirect_url = google.build_url(request, '__account_google_authenticated')
        payload = google.verify_auth(request, redirect_url)
        self.save_connection(self.request, payload)
        return redirect(REDIRECT_URI_NAME)

    @transaction.atomic
    def save_connection(self, request, payload):
        try:
            google = Google()
            email = google.validate_id_token(payload.get('id_token'))

            if not email:
                return False

            data = {
                'id_token': payload.get('id_token'),
                'access_token': payload.get('access_token'),
                'expires_in': payload.get('expires_in'),
                'refresh_token': payload.get('refresh_token', None),
                'token_type': payload.get('token_type'),
            }

            user = request.user if not request.user.is_anonymous else None

            if not user:
                is_exist = GoogleModel.objects.filter(identifier=email).first()
                if not is_exist:
                    payload = {
                        'username': self.clear_username(request, email.split('@')[0].split('+')[0])
                    }
                    user = get_user_model().objects.create_user(**payload)
                    data.update({'user': user})
                else:
                    user = is_exist.user
                GoogleModel.objects.update_or_create(identifier=email, defaults=data)
                login(request, user)
            else:
                data.update({
                    'identifier': email,
                })
                is_another_account = GoogleModel.objects.filter(email=email).first()
                if is_another_account:
                    messages.error(self.request, _('account_with_this_connection_already_exist'))
                    return False
                GoogleModel.objects.update_or_create(user=user, defaults=data)
        except Exception as e:
            logging.error(str(e))

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
        google = Google()
        google.revoke_token(request.user)
        return redirect(REDIRECT_URI_NAME)
