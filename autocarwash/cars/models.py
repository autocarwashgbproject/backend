from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Car(models.Model):  # Модель автомобиля клиента
    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = "Автомобили"

    car_num = models.CharField(verbose_name='Номер автомобиля', db_index=True, unique=True, max_length=32)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
