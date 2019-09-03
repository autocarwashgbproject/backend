from django.db import models
# Create your models here.

class City(models.Model):
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = "Города"

    city = models.CharField(verbose_name='Город', unique=True, max_length=100)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    delete_date = models.DateTimeField(verbose_name='Удален', null=True, blank=True)


class Wash(models.Model):
    class Meta:
        verbose_name = 'Мойка'
        verbose_name_plural = "Мойки"

    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)
    adress = models.CharField(verbose_name='Адрес', unique=True, max_length=150)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    delete_date = models.DateTimeField(verbose_name='Удален', null=True, blank=True)


class Subscription(models.Model):
    class Meta:
        verbose_name = 'Тарифный план'
        verbose_name_plural = "Тарифные планы"

    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)
    subscription = models.CharField(verbose_name='Тарифный план', unique=True, max_length=45)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    delete_date = models.DateTimeField(verbose_name='Удален', null=True, blank=True)

    def subscription_price(): # TODO
        a = 2000
        return a


class Sevice(models.Model):
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = "Услуги"

    subscription = models.ForeignKey(Subscription, verbose_name='Тарифный план', on_delete=models.CASCADE)
    sevice = models.CharField(verbose_name='Имя услуги', unique=True, max_length=45)
    price = models.DecimalField(verbose_name='Цена услуги', max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    delete_date = models.DateTimeField(verbose_name='Удален', null=True, blank=True)
