from django.db import models
from django.contrib.auth import get_user_model


class Google(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    identifier = models.BigIntegerField(unique=True)
    id_token = models.TextField()
    token_type = models.CharField(max_length=50)
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500, default=None, null=True)
    expires_in = models.PositiveBigIntegerField()
    email = models.EmailField(unique=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Google'

    def __str__(self):
        user = str(self.user)
        return f'Google Connection - {user.capitalize()}'
