from . import service_template
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import redirect
from ...utils.forms import EditProfileForm
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView
from django.contrib.auth.decorators import login_required
from ...models import Profile, Google, Steam, Twitch, Discord


@method_decorator(decorator=login_required, name='dispatch')
class Index(TemplateView):
    template_name = f'{service_template}/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        google = Google.objects.filter(user=self.request.user)
        steam = Steam.objects.filter(user=self.request.user)
        twitch = Twitch.objects.filter(user=self.request.user)
        discord = Discord.objects.filter(user=self.request.user)
        context.update({
            'edit_form': EditProfileForm,
            'google': google,
            'steam': steam,
            'twitch': twitch,
            'discord': discord,
        })

        return context


@method_decorator(decorator=login_required, name='dispatch')
class Edit(FormView):
    success_url = reverse_lazy('__account_profile_index')
    form_class = EditProfileForm

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['edit_form'] = EditProfileForm
        return context

    def form_invalid(self, form):
        return JsonResponse({'status': False, 'errors': form.errors}, status=422)

    def form_valid(self, form):
        profile_data = form.cleaned_data
        obj, created = Profile.objects.update_or_create(user=self.request.user, defaults={
            'gender': profile_data.get('gender'),
            'date_of_birth': profile_data.get('date_of_birth'),
            'phone_number': profile_data.get('phone_number')
        })
        if obj:
            get_user_model().objects.filter(pk=self.request.user.pk).update(
                first_name=profile_data.get('first_name'),
                last_name=profile_data.get('last_name')
            )
        return JsonResponse({'status': True, 'url': self.success_url}, status=200)
