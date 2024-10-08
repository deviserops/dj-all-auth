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


class EditProfileForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=50)
    last_name = forms.CharField(required=True, max_length=50)
    email = forms.CharField(required=False, max_length=150)
