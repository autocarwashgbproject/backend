import calendar
from datetime import datetime as dt

from django.db import models
from django.contrib.auth import get_user_model
from subscription.models import Subscription
from django.core.validators import RegexValidator

User = get_user_model()


class Car(models.Model):
    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = "Автомобили"

    car_num_regex = RegexValidator(
        regex=r'^[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ][АВЕКМНОРСТУХ]\d{2,3}$',
        message='Неверный формат номера автомобиля'
    )

    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE,
        related_name="users"
        )
    subscription = models.ForeignKey(
        Subscription, verbose_name='Тарифный план', on_delete=models.CASCADE,
        null=True, blank=True
        )
    reg_num = models.CharField(
        validators=[car_num_regex], db_index=True, unique=True, max_length=9
        )
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(
        verbose_name='Создан', auto_now_add=True
        )
    update_date = models.DateTimeField(
        verbose_name='Обновлен', auto_now=True
        )
    delete_date = models.DateTimeField(
        verbose_name='Удален', null=True, blank=True
        )
    is_regular_pay = models.BooleanField(default=False)

def sub_date_plus_month(datetime):
    month = datetime.month
    year = datetime.year + month // 12
    month = month % 12 + 1
    day = min(datetime.day, calendar.monthrange(year,month)[1])

    return dt(year, month, day)

class SubscriptionCar(models.Model):
    class Meta:
        verbose_name = 'Подписку автомобиля'
        verbose_name_plural = "Подписки автомобиля"

    reg_num = models.ForeignKey(
        Car, verbose_name='Номер автомобиля', on_delete=models.CASCADE
        )
    subscription = models.ForeignKey(
        Subscription, verbose_name='Тарифный план', on_delete=models.CASCADE
        )
    subscription_date = models.DateTimeField(auto_now_add=True)

    def is_subscribe(sub_date_plus_month):
        if dt.now().replace(tzinfo=None) <= sub_date_plus_month.replace(tzinfo=None):
            return True
        else:
            return False
