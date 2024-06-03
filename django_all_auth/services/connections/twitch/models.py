from django.db import models
from django.contrib.auth import get_user_model


class Twitch(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    token_type = models.CharField(max_length=50)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500, default=None, null=True)
    expires_in = models.PositiveBigIntegerField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Twitch'

    def __str__(self):
        user = str(self.user)
        return f'Twitch Connection - {user.capitalize()}'
