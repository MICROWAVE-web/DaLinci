from __future__ import unicode_literals

import random
import string

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _  # Почитать


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    date_joined = None
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_('password'), max_length=50)
    reg_time_and_date = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['is_superuser', 'last_login']


class AbbreviatedLink(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    created_time_and_date = models.DateTimeField(auto_now_add=True)
    parent_link = models.URLField(_('url'), max_length=300)
    counter = models.PositiveIntegerField(default=0)
    urlhash = models.CharField(max_length=6, null=True, blank=True, unique=True)

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
        if not self.urlhash:
            self.urlhash = self.id_generator()
            while AbbreviatedLink.objects.filter(urlhash=self.urlhash).exists():
                self.urlhash = self.id_generator()
        super(AbbreviatedLink, self).save()

    class Meta:
        unique_together = ('owner', 'parent_link')


class Transition(models.Model):
    ip = models.GenericIPAddressField()
    time_and_date = models.DateTimeField(auto_now_add=True)
    abbr_link = models.ForeignKey(AbbreviatedLink, on_delete=models.PROTECT)
