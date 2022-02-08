from __future__ import unicode_literals

import random
import string

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# from django.utils.translation import ugettext_lazy as _  # Почитать


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    date_joined = None
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = PhoneNumberField(validators=[phone_regex], verbose_name='Номер телефона', null=False, blank=False,
                             unique=True)
    password = models.CharField(verbose_name='Пароль', max_length=50)
    reg_time_and_date = models.DateTimeField(auto_now_add=True)
    personal_sms_code = models.IntegerField(null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['is_superuser', 'last_login']

    @staticmethod
    def sms_code_generator(size=6, chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
        if not self.personal_sms_code:
            self.personal_sms_code = self.sms_code_generator()
        super(User, self).save()


class AbbreviatedLink(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_time_and_date = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    parent_link = models.URLField(max_length=300, verbose_name='URL')
    counter = models.PositiveIntegerField(default=0, verbose_name='Счетчик')
    urlhash = models.CharField(max_length=6, null=True, blank=True, unique=True, verbose_name='Персональный код')

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
    ip = models.GenericIPAddressField(verbose_name='IP адресс пользователя')
    time_and_date = models.DateTimeField(auto_now_add=True, verbose_name='Время перехода')
    abbr_link = models.ForeignKey(AbbreviatedLink, on_delete=models.CASCADE)
