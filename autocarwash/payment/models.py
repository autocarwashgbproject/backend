from django.db import models
from car.models import SubscriptionCar

# Create your models here.

class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"

    subscription_car = models.ForeignKey(SubscriptionCar, verbose_name='Тарифный план', on_delete=models.CASCADE)
    order = models.DateTimeField(verbose_name='Заказ', auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    delete_date = models.DateTimeField(verbose_name='Удален', null=True)

    def is_paid():
        pass
