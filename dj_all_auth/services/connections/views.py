from . import connections_template
from django.views.generic import TemplateView
from ...models import Google, Steam, Twitch, Discord


class Index(TemplateView):
    template_name = connections_template + '/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        google = Google.objects.filter(user=self.request.user)
        steam = Steam.objects.filter(user=self.request.user)
        twitch = Twitch.objects.filter(user=self.request.user)
        discord = Discord.objects.filter(user=self.request.user)
        context.update({
            'google': google,
            'steam': steam,
            'twitch': twitch,
            'discord': discord,
        })

        return context
