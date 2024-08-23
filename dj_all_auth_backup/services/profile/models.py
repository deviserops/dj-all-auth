from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class Profile(models.Model):
    MALE = 'MA'
    FEMALE = 'FM'
    OTHER = 'OT'
    genders = [
        (MALE, _('male')),
        (FEMALE, _('female')),
        (OTHER, _('other'))
    ]
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image_url = models.URLField(null=True, blank=True, db_comment='Profile image url of user.')
    gender = models.CharField(max_length=3, choices=genders, null=True, default=None)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, db_comment='Include with country code.', null=True)

    def __str__(self):
        return f'{self.user.username}'
