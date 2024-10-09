from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# make default email to unique
get_user_model()._meta.get_field('email')._unique = True


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class AccountActivateForm(forms.Form):
    email = forms.EmailField()
