from __future__ import unicode_literals

import random
import string

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField


# from django.utils.translation import ugettext_lazy as _  # Почитать


import random
import string
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер для управления пользователями."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Отключение поля username
    first_name = None  # Удаление first_name
    last_name = None  # Удаление last_name
    date_joined = None  # Удаление date_joined

    email = models.EmailField(verbose_name='Email', unique=True)  # Основное поле для логина
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be: '+999999999'.")
    password = models.CharField(verbose_name='Password', max_length=1000)
    reg_time_and_date = models.DateTimeField(auto_now_add=True)
    personal_sms_code = models.IntegerField(null=True, blank=True)

    # Настройка полей для авторизации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Уберите 'is_superuser' и 'last_login', их не нужно задавать вручную

    objects = UserManager()  # Используем пользовательский менеджер

    @staticmethod
    def sms_code_generator(size=6, chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
        if not self.personal_sms_code:
            self.personal_sms_code = self.sms_code_generator()
        super(User, self).save(*args, **kwargs)


class AbbreviatedLink(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_time_and_date = models.DateTimeField(auto_now_add=True, verbose_name='Creation time')
    parent_link = models.URLField(max_length=300, verbose_name='URL')
    counter = models.PositiveIntegerField(default=0, verbose_name='Counter')
    urlhash = models.CharField(max_length=6, null=True, blank=True, unique=True, verbose_name='Personal identification code')

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
    ip = models.GenericIPAddressField(verbose_name='The user\'s IP address')
    time_and_date = models.DateTimeField(auto_now_add=True, verbose_name='Transition time')
    abbr_link = models.ForeignKey(AbbreviatedLink, on_delete=models.CASCADE)
