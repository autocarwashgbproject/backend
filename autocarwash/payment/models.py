from django.db import models
from car.models import Car
from django.contrib.auth import get_user_model
from subscription.models import Subscription

User = get_user_model()


class CardBankUsers(models.Model):
    timestamp = models.DateTimeField(
        verbose_name='Создан', auto_now_add=True
        )
    payment_id = models.CharField(
        verbose_name='id оплаты', db_index=True, unique=True, max_length=50,
        blank=True, null=True
        )
    last4 = models.CharField(
        verbose_name='Последние 4 цифры карты', max_length=4, blank=True,
        null=True
        )
    card_type = models.CharField(
        verbose_name='Тип платежной системы', max_length=25, blank=True,
        null=True
        )
    bank = models.CharField(
        verbose_name='Банк', max_length=75, blank=True, null=True
        )
    payment_method_saved = models.BooleanField(default=False)

class BankUsers(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE
        )
    card_bank_users = models.ForeignKey(
        CardBankUsers, verbose_name='Банковские данные пользователя',
        on_delete=models.CASCADE, related_name="cards_bank_users"
        )
    timestamp = models.DateTimeField(verbose_name='Создан', auto_now_add=True)

class OrderBankUsers(models.Model):
    # TODO подмуать над значениями max_length=15 в error, error_description
    card_bank_users = models.ForeignKey(
        CardBankUsers, verbose_name='Какой картой оплачивали',
        on_delete=models.CASCADE, related_name="order_cards_bank_users"
        )
    car = models.ForeignKey(
        Car, verbose_name='Машина', on_delete=models.CASCADE,
        related_name="cars"
        )
    subscription = models.ForeignKey(
        Subscription, verbose_name='Подписка', on_delete=models.CASCADE,
        related_name="subscriptions"
        )
    timestamp = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    update = models.DateTimeField(
        verbose_name='Изменили', auto_now=True, blank=True, null=True
        )
    is_regular_pay = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    error = models.CharField(
        verbose_name='Ошибка', max_length=35, blank=True, null=True
        )
    error_description = models.CharField(
        verbose_name='Описание ошибок', max_length=80, blank=True, null=True
        )
    payment_method_saved = models.BooleanField(default=False)
    recipient_account_id = models.CharField(
        verbose_name='account_id', max_length=15, blank=True, null=True
        )
    recipient_gateway_id = models.CharField(
        verbose_name='gateway_id', max_length=15, blank=True, null=True
        )
    refundable = models.BooleanField(default=False)
    status = models.CharField(
        verbose_name='Статус платежа', max_length=15, blank=True, null=True
        )
    created_at = models.DateTimeField(
        verbose_name='Запрос на оплату', blank=True, null=True
        )
