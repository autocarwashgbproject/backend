from datetime import datetime as dt

from rest_framework import serializers

from .models import Car, SubscriptionCar, sub_date_plus_month
from client.models import User


class CarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'reg_num', 'user')

    def to_representation(self, data):
        instance = super(CarListSerializer, self).to_representation(data)
        instance['ok'] = True
        if instance['timestamp']:
            instance['timestamp'] = User.format_date_to_unix(
                instance['timestamp']
                )
        if instance['update_date']:
            instance['update_date'] = User.format_date_to_unix(
                instance['update_date']
                )
        return instance

class CarDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Car
        fields = (
            'id', 'reg_num', 'user', 'is_regular_pay', 'timestamp',
            'update_date'
            )

    def to_representation(self, data):
        instance = super(CarDetailSerializer, self).to_representation(data)
        instance['ok'] = True
        subscription_date = SubscriptionCar.objects.filter(
            reg_num = instance['id']).order_by('-subscription_date'
            )
        if subscription_date.exists():
            last_subscription_date = subscription_date.first().subscription_date
            # format: 2019-09-04 21:05:51.186224+00:00 TESTS (предполодим,
            # что клиент оформила подписку): last_subscription_date =
            # dt(2019, 1, 31)
            subscription_date_validation = sub_date_plus_month(
                datetime=last_subscription_date
                )
            instance['is_subscribe'] = SubscriptionCar.is_subscribe(
                sub_date_plus_month=subscription_date_validation
                )
            instance['subscription_date'] = int(
                (last_subscription_date.replace(tzinfo=None) - \
                    dt(1970, 1, 1)
                    ).total_seconds()
                )
            instance['subscription_date_validation'] = int(
                (subscription_date_validation.replace(tzinfo=None) - \
                    dt(1970, 1, 1)
                    ).total_seconds()
                )
        else:
            instance['is_subscribe'] = False
        if instance['timestamp']:
            instance['timestamp'] = User.format_date_to_unix(
                instance['timestamp']
                )
        if instance['update_date']:
            instance['update_date'] = User.format_date_to_unix(
                instance['update_date']
                )
        return instance
