from django.db import models
from django.utils.translation import gettext as _


class EmailTemplate(models.Model):
    RESET_PASSWORD = 'REP'
    REGISTER = 'REG'
    REQUEST_ACCOUNT_ACTIVATION = 'RAA'
    names = [
        (RESET_PASSWORD, _('reset_password')),
        (REGISTER, _('register')),
        (REQUEST_ACCOUNT_ACTIVATION, _('request_account_activation'))
    ]
    template = models.CharField(max_length=5, choices=names, unique=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.get_template_display()}"
