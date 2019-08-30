from django.db import models
from car.models import Car, SubscriptionCar
from subscription.models import Wash
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Washing(models.Model):
    class Meta:
        verbose_name = 'Помывка'
        verbose_name_plural = "Помывки"

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, verbose_name='Автомобиль', on_delete=models.CASCADE)
    wash = models.ForeignKey(Wash, verbose_name='Помывка', on_delete=models.CASCADE)
    washing = models.CharField(verbose_name='Комментарий к помывке', max_length=20)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
