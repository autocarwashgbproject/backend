from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

import random
import os
import requests
from datetime import datetime


# User.object.create_user(phone='123123123123', password='123hjk8gcn')
class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('Пользователь должен иметь номер телефона')
        if not password:
            raise ValueError('Пользователь должен иметь пароль')

        user_obj = self.model(
            phone=phone
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(
            using=self._db
        )
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,

        )
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class User(AbstractBaseUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$', # TODO
        message='Номер телефона необходимо вводить в формате: «+79031234567». Допускается до 14 цифр.'
    )
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    surname = models.CharField(max_length=20, blank=True, null=True)
    patronymic = models.CharField(verbose_name='Отчество', max_length=20, blank=True, null=True)
    birthday = models.DateField(verbose_name='День рождения', null=True)
    email = models.EmailField(verbose_name='E-mail', blank=True, null=True)
    first_login = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    delete_date = models.DateTimeField(verbose_name='Удален', null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # конвертируем дату в формат unix
    def format_date_to_unix(date):
        try:
            datet = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            datet = datetime.strptime(date, '%Y-%m-%d')

        timestamp = (datet - datetime(1970, 1, 1)).total_seconds()

        return int(timestamp)

    # конвертируем дату в формат бд
    def format_date_to_base(date):
        # ISO 8601
        datet = datetime.fromtimestamp(date)
        date = datet.strftime('%Y-%m-%d')

        return date

    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.name:
            return self.name
        else:
            return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$',
        message='Номер телефона необходимо вводить в формате: «+79031234567». Допускается до 14 цифр.'
    )
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Количетсво отправленных кодов проверки')

    # logged = models.BooleanField(default=False, help_text='Если проверка кодов прошла успешно')
    # forgot = models.BooleanField(default=False, help_text='Верно только для забытого пароля')
    # forgot_logged = models.BooleanField(default=False, help_text='only true if validate otp forgot get successful')

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)
