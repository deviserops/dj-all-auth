import logging

from ...lib.Mail import Mail
from ... import base_template
from ...models import Profile
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView
from django.template.loader import get_template
from django.utils.translation import gettext as _
from django.views.generic import CreateView, View
from ...utils.TokenGenerator import TokenGenerator
from ...utils.forms import RegisterForm, AccountActivateForm
from ...context_processors import __default_context as default_context


class Register(CreateView):
    model = get_user_model()
    template_name = base_template + '/auth/register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_invalid(self, form):
        return JsonResponse({'status': False, 'errors': form.errors}, status=422)

    def form_valid(self, form):
        user = form.save(False)
        user.is_active = False
        user.save()

        # create profile for user
        profile = Profile()
        profile.user = user
        profile.save()

        # send verification mail
        self.send_email(user)

        messages.success(self.request, _('active_your_account_with_email'))
        return JsonResponse({'status': True, 'url': reverse('home')}, status=200)

    def send_email(self, user):
        # Send Account activation mail
        token_generator = TokenGenerator()
        token_info = token_generator.generate_token(user)

        link = reverse("__activate_account",
                       kwargs={"uidb64": token_info.get('uidb64'), "token": token_info.get('token')})
        context = {
            'link': link,
            'user': user
        }
        context.update(default_context(self.request))
        text_content = get_template(f'{base_template}/mail/register/mail.text').render(context)
        args = {
            'subject': _('email_subject_active_request'),
            'to': [user.email],
            'text_content': text_content
        }
        Mail(multipart=True).send_mail(args)


class ActivateAccount(View):
    def get(self, request, uidb64, token):
        try:
            token_generator = TokenGenerator()
            url_hash = token_generator.decode_uid(uidb64)
            user_hash = url_hash.split('|')
            user = get_user_model().objects.filter(id=user_hash[0], username=user_hash[1], email=user_hash[2],
                                                   is_active=False).first()
            if user:
                token_generator = TokenGenerator()
                verify = token_generator.verify_token(user, token)
                if verify:
                    user.is_active = True
                    user.save()
                    messages.info(request, _('account_activated_can_login'))
                else:
                    messages.error(request, _('invalid_token'))
            else:
                messages.error(request, _('no_user_found'))
        except Exception as e:
            logging.error(e)
            messages.error(request, _('something_went_wrong'))
        return redirect('login')


class ActivateRequest(FormView):
    form_class = AccountActivateForm
    template_name = base_template + '/auth/request_account_activation.html'

    def form_invalid(self, form):
        return JsonResponse({'status': False, 'errors': form.errors}, status=422)

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            user = get_user_model().objects.filter(email=data.get('email'), is_active=False).first()
            if user:
                token_generator = TokenGenerator()
                token_info = token_generator.generate_token(user)
                link = reverse("__activate_account",
                               kwargs={"uidb64": token_info.get('uidb64'), "token": token_info.get('token')})
                context = {
                    'link': link,
                    'user': user
                }
                context.update(default_context(self.request))
                text_content = get_template(f'{base_template}/mail/activate_request/mail.text').render(context)
                args = {
                    'subject': _('email_subject_active_request'),
                    'to': [user.email],
                    'text_content': text_content,
                }
                Mail(multipart=True).send_mail(args)

                messages.info(self.request, _('active_your_account_with_email'))
                return JsonResponse({'status': True, 'url': reverse('login')}, status=200)
            else:
                return JsonResponse({'status': False, 'message': _('account_with_email_not_exist')}, status=422)
        except Exception as e:
            logging.error(e)
            return JsonResponse({'status': False, 'message': _('something_went_wrong')}, status=422)
