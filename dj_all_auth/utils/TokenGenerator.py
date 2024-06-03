from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator:
    def generate_token(self, user):
        user_hash = f'{user.pk}|{user.username}|{user.email}|{user.is_active}'
        uid_64 = urlsafe_base64_encode(force_bytes(user_hash))

        account_activation_token = PasswordResetTokenGenerator()
        token = PasswordResetTokenGenerator.make_token(self=account_activation_token, user=user)

        token_info = {
            'uidb64': uid_64,
            'token': token
        }
        return token_info

    def verify_token(self, user, token):
        account_activation_token = PasswordResetTokenGenerator()
        return PasswordResetTokenGenerator.check_token(self=account_activation_token, user=user, token=token)

    def decode_uid(self, uidb64):
        return force_str(urlsafe_base64_decode(uidb64))
