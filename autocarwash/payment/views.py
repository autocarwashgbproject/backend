from django.shortcuts import render, redirect
from django.views.generic.base import View
from autocarwash.secrets import BANK_CLIENT_ID, BANK_CLIENT_SECRET, BANK_KEY_SECRET, BANK_ACCOUNT_ID, SITE_URL
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from .permissions import IsOwner
from .models import OrderBankUsers, BankUsers, CardBankUsers
from car.models import Car, SubscriptionCar, sub_date_plus_month
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import requests, uuid, time
from datetime import datetime, timedelta
from client.models import User
from yandex_checkout import Configuration, Settings, Webhook, Payment
from subscription.models import Subscription
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .serializers import ViewPaymentSerializer, ViewCardsSerializer

# Create your views here.


class PaymentDetailView(generics.GenericAPIView):
    # authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, ) # IsOwner

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        bankusers = BankUsers.objects.filter(user=pk)
        data = list()
        for i in bankusers:
            orderbankusers = OrderBankUsers.objects.filter(card_bank_users=i.id)
            serializer = ViewPaymentSerializer(orderbankusers, many=True)
            data.append(*serializer.data)

        return Response({
            "ok":True,
            "payment": data
        })

class CardsDetailView(generics.GenericAPIView):
    # authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, ) # IsOwner

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        bankusers = BankUsers.objects.filter(user=pk)
        data = list()
        for i in bankusers:
            cardbankusers = CardBankUsers.objects.filter(id=i.id)
            serializer = ViewCardsSerializer(cardbankusers, many=True)
            data.append(*serializer.data)

        return Response({
            "ok":True,
            "cards": data
        })


def card_update(user_card, payment):
    # сохраняем данные запроса в CardBankUsers
    # user_card.bank = payment.payment_method.card.issuer_name # TODO для тестов убираем, так как не приходит название банка
    user_card.card_type = payment.payment_method.card.card_type
    user_card.last4 = payment.payment_method.card.last4
    user_card.payment_id = payment.id
    user_card.payment_method_saved = payment.payment_method.saved
    user_card.save()


def order_update(order, payment):
    # сохраняем данные запроса в OrderBankUsers
    order.status = payment.status
    order.is_paid = payment.paid
    order.payment_method_saved = payment.payment_method.saved
    order.recipient_gateway_id = payment.recipient.gateway_id
    order.recipient_account_id = payment.recipient.account_id
    order.refundable = payment.refundable
    order.created_at = payment.created_at
    try:
        order.error = payment.cancellation_details.payment_network
        order.error_description = payment.cancellation_details.payment_method_restricted
    except Exception as e:
        pass

    # TODO
    # error = models.CharField(verbose_name='Ошибка', max_length=10, blank=True, null=True)
    # error_description = models.CharField(verbose_name='Описание ошибок', max_length=15, blank=True, null=True)
    order.save()


class PayCreateView(APIView):
    # authentication_classes = (TokenAuthentication, ) TODO
    permission_classes = (AllowAny, ) # IsOwner TODO

    def post(self, request, *args, **kwargs):
        car_id = request.data.get('car_id')
        is_regular_pay = request.data.get('is_regular_pay')
        user_card_id = request.data.get('user_card_id')
        subscription = Subscription.objects.get(id=1) # пока только 1 подписка TODO

        if car_id and isinstance(is_regular_pay, bool):
            car = Car.objects.get(id=car_id)
            if user_card_id == None:
                user = car.user
                bank_users = BankUsers.objects.filter(user=user)
                if bank_users.exists():
                    user_card = list()
                    for i in bank_users:
                        user_card.append(i.id)

                    return Response({
                        'ok': False,
                        'error': 452,
                        'error_description': "No user_card_id",
                        'car_id': car_id,
                        'is_regular_pay': is_regular_pay,
                        'user_card_id': user_card
                    })
                else:
                    user_card = CardBankUsers.objects.create()
                    BankUsers.objects.create(user=user, card_bank_users=user_card)

                    return Response({
                        'ok': False,
                        'error': 404,
                        'error_description': "user_card_id was created",
                        'car_id': car_id,
                        'is_regular_pay': is_regular_pay,
                        'user_card_id': [user_card.id]
                    })

            if is_regular_pay:
                car.is_regular_pay = is_regular_pay
                car.save()

            is_subscribe = False
            subscription_date = SubscriptionCar.objects.filter(reg_num = car).order_by('-subscription_date')

            if subscription_date.exists():
                last_subscription_date = subscription_date.first().subscription_date
                subscription_date_validation = sub_date_plus_month(datetime=last_subscription_date)
                is_subscribe = SubscriptionCar.is_subscribe(sub_date_plus_month=subscription_date_validation)

            if is_subscribe:
                return Response({
                    'ok': False,
                    'pay': True,
                    'description': "Arleady subscribe"
                })
            else:
                value = subscription.subscription_price()
                user_card = CardBankUsers.objects.filter(id=user_card_id).order_by('-timestamp')
                user_card = user_card.first()
                order = OrderBankUsers.objects.create(card_bank_users=user_card, car=car, is_regular_pay=is_regular_pay, subscription=subscription)

                if user_card.payment_method_saved:
                    payment_id = user_card.payment_id
                    yandex_pay = YandexPay(payment_id=payment_id)
                    payment = yandex_pay.pay_with_payment_id(order=order, value=value)
                    order_update(order=order, payment=payment)
                    user_card.payment_id = payment.payment_method.id
                    user_card.save()
                    check_pay = yandex_pay.check_pay(payment_id=user_card.payment_id)
                    order_update(order=order, payment=check_pay)
                    card_update(user_card=user_card, payment=check_pay)
                    if check_pay.paid:
                        car = Car.objects.get(id=car_id)
                        SubscriptionCar.objects.create(reg_num=car, subscription=subscription)
                        return Response({
                            'ok': True,
                            'pay': True,
                            'description': "Оплачено"
                        })
                    else:
                        return Response({
                            'ok': False,
                            'pay': False,
                            'description': "Не олачено"
                        })
                else:
                    yandex_pay = YandexPay()
                    payment = yandex_pay.pay_without_payment_id(order=order, value=value)
                    order_update(order=order, payment=payment)
                    user_card.payment_id = payment.payment_method.id
                    user_card.save()

                    # TODO если человек не нажмет после яндекс оплаты вернутся в магазин, то оплату не проверим,
                    # соответственно не будет подписки у клиента и оплаты проверенной, в связи с этим надо запускать ResultCreateView
                    # самостоятельно по опредленным ид, которые в течении последних 5 минут запросили оплату, запускать каждые 3 минуты (то есть по всем новым OrderBankUsers)

                    return Response({
                        'ok': True,
                        'site': payment.confirmation.confirmation_url
                    })
        # если нету car_id, is_regular_pay
        else:
            return Response({
                'ok': False,
                'error_code': 404,
                'description': "We can't see car_id or is_regular_pay or user_card_id or all of them"
            })



class ResultCreateView(View):

    def get(self, request, *args, **kwargs):
        order_id = kwargs['pk']
        order = OrderBankUsers.objects.get(id=order_id)
        if order.is_paid:
            context = {
                'pay': "Оплачено"
            }
        else:
            payment_id = order.card_bank_users.payment_id
            yandex_pay = YandexPay()
            check_pay = yandex_pay.check_pay(payment_id=payment_id)
            if check_pay == False:
                context = {
                    'pay': f"Вы еще не провели оплату, вернутся на страницу оплаты: https://money.yandex.ru/payments/external/confirmation?orderId={order.card_bank_users.payment_id}"
                }
                return render(request, 'payment/index.html', context)
            print()
            for key, val in check_pay:
                print(f"{key}: {val}")
            print()
            order_update(order=order, payment=check_pay)
            card_update(user_card=order.card_bank_users, payment=check_pay)
            if check_pay.paid:
                SubscriptionCar.objects.create(reg_num=order.car, subscription=order.subscription)
                context = {
                    'pay': "Оплачено"
                }
            else:
                context = {
                    'pay': "Не олачено"
                }

        return render(request, 'payment/index.html', context)


class YandexPay():
    """docstring for Pay."""

    def __init__(self, payment_id=None):
        self.site_url = SITE_URL
        self.payment_id = payment_id

        # authorization
        Configuration.account_id = BANK_ACCOUNT_ID
        Configuration.secret_key = BANK_KEY_SECRET
        # данные по приложению
        self.settings = Settings.get_account_settings()

    def pay_with_payment_id(self, order, value):
        payment = Payment.create({
            "amount": {
                "value": value,
                "currency": "RUB"
            },
            "description": f"Заказ {order.id}",
            "payment_method_id": self.payment_id

        }, str(uuid.uuid4()))

        return payment

    def pay_without_payment_id(self, order, value):
        return_url = f"{self.site_url}pay/{order.id}/"

        payment = Payment.create({
            "amount": {
              "value": value,
              "currency": "RUB"
            },
            "capture": True,
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
            "description": f"Заказ {order.id}",
            "save_payment_method": True,
            "metadata": {
                "order_id": order.id
            }
        }, str(uuid.uuid4()))

        return payment

    def check_pay(self, payment_id):
        paid = False
        time_while_end = datetime.now() + timedelta(seconds=33)
        while paid == False and datetime.now(tz=None) <= time_while_end:
            payment_result = Payment.find_one(payment_id)
            paid = payment_result.paid
            time.sleep(3)

        if paid:
            paid = payment_result

        return paid
