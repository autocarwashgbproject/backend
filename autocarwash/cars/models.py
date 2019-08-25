from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Car(models.Model):  # Модель автомобиля клиента
    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = "Автомобили"

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    reg_num = models.CharField(verbose_name='Номер автомобиля', db_index=True, unique=True, max_length=9)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    delete_date = models.DateTimeField(verbose_name='Удален', null=True)
