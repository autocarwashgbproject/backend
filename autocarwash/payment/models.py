from django.db import models
from car.models import Car
from django.contrib.auth import get_user_model
from subscription.models import Subscription

User = get_user_model()

# Create your models here.
class CardBankUsers(models.Model):
    timestamp = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    payment_id = models.CharField(verbose_name='id оплаты', db_index=True, unique=True, max_length=50, blank=True, null=True)
    last4 = models.CharField(verbose_name='Последние 4 цифры карты', max_length=4, blank=True, null=True)
    card_type = models.CharField(verbose_name='Тип платежной системы', max_length=35, blank=True, null=True)
    bank = models.CharField(verbose_name='Банк', max_length=50, blank=True, null=True)


class BankUsers(models.Model):
    # TODO подмуать над значениями max_length=50 в моделях и проверка на параметры в моделях
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    card_bank_users = models.ForeignKey(CardBankUsers, verbose_name='Банковские данные пользователя', on_delete=models.CASCADE, related_name="cards_bank_users")
    timestamp = models.DateTimeField(verbose_name='Создан', auto_now_add=True)


class OrderBankUsers(models.Model):
    card_bank_users = models.ForeignKey(CardBankUsers, verbose_name='Какой картой оплачивали', on_delete=models.CASCADE, related_name="order_cards_bank_users")
    car = models.ForeignKey(Car, verbose_name='Машина', on_delete=models.CASCADE, related_name="cars")
    subscription = models.ForeignKey(Subscription, verbose_name='Подписка', on_delete=models.CASCADE, related_name="subscriptions")
    timestamp = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    update = models.DateTimeField(verbose_name='Изменили', auto_now=True, blank=True, null=True)
    is_regular_pay = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    error = models.CharField(verbose_name='Ошибка', max_length=10, blank=True, null=True)
    error_description = models.CharField(verbose_name='Описание ошибок', max_length=15, blank=True, null=True)
    payment_method_saved = models.BooleanField(default=False)
    recipient_account_id = models.CharField(verbose_name='account_id', max_length=15, blank=True, null=True)
    recipient_gateway_id = models.CharField(verbose_name='gateway_id', max_length=15, blank=True, null=True)
    refundable = models.BooleanField(default=False)
    status = models.CharField(verbose_name='Статус платежа', max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Запрос на оплату', blank=True, null=True)


# amount: {'currency': 'RUB', 'value': 2000.01}
# confirmation: {'confirmation_url': 'https://money.yandex.ru/payments/external/confirmation?orderId=2508e347-000f-5000-a000-1cdeb356132c', 'return_url': 'http://127.0.0.1:8000/return_url', 'type': 'redirect'}
# created_at: 2019-09-09T22:17:43.185Z
# description: Заказ 15
# id: 2508e347-000f-5000-a000-1cdeb356132c
# metadata: {'order_id': '15'}
# paid: False
# payment_method: {
#   'id': '2508e347-000f-5000-a000-1cdeb356132c',
#   'saved': False,
#   'type': 'bank_card',
#   "title": "Bank card *4444",
#    "card": {
#      "first6": "555555",
#      "last4": "4444",
#      "expiry_month": "07",
#      "expiry_year": "2022",
#      "card_type": "MasterCard",
#      "issuer_country": "RU",
#      "issuer_name": "Sberbank"
#    }
# }
# recipient: {'account_id': '634986', 'gateway_id': '1625970'}
# refundable: False
# status: pending
# test: True
