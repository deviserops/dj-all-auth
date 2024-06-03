from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . import service_template


@method_decorator(decorator=login_required, name='dispatch')
class Index(TemplateView):
    template_name = f'{service_template}/index.html'
