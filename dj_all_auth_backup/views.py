from . import base_template
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(decorator=login_required, name='dispatch')
class Index(TemplateView):
    template_name = f'{base_template}/index.html'
