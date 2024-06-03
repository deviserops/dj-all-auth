from django.db import models
from django.contrib.auth import get_user_model


class Steam(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    steam_id = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Steam'

    def __str__(self):
        user = str(self.user)
        return f'Steam Connection - {user.capitalize()}'
