from . import profile_template
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import redirect
from ...utils.forms import EditProfileForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


@method_decorator(decorator=login_required, name='dispatch')
class Index(TemplateView):
    template_name = f'{profile_template}/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'profile_form': EditProfileForm,
            'password_change_form': PasswordChangeForm(self.request.user)
        })

        return context


@method_decorator(decorator=login_required, name='dispatch')
class ProfileEdit(FormView):
    success_url = reverse_lazy('__account')
    form_class = EditProfileForm

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile_form'] = EditProfileForm
        return context

    def form_invalid(self, form):
        return JsonResponse({'status': False, 'errors': form.errors}, status=422)

    def form_valid(self, form):
        profile_data = form.cleaned_data
        email = self.request.user.email if self.request.user.email else profile_data.get('email')
        get_user_model().objects.filter(pk=self.request.user.pk).update(
            first_name=profile_data.get('first_name'),
            last_name=profile_data.get('last_name'),
            email=email
        )

        return JsonResponse({'status': True, 'url': None, 'message': _('profile_updated')}, status=200)


@method_decorator(decorator=login_required, name='dispatch')
class PasswordEdit(PasswordChangeView):

    def form_invalid(self, form):
        return JsonResponse({'status': False, 'errors': form.errors}, status=422)

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return JsonResponse({'status': True, 'url': None, 'message': _('password_updated')}, status=200)
