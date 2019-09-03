from rest_framework import serializers
from .models import Subscription


class SubscriptionListSerializer(serializers.ModelSerializer):  # Список всех машин
    class Meta:
        model = Subscription
        fields = ('id', 'city', 'subscription', )

    def to_representation(self, data):
        instance = super(SubscriptionListSerializer, self).to_representation(data)


        instance['subscription_price'] = Subscription.subscription_price()
        # if instance['timestamp']:
        #     instance['timestamp'] = User.format_date_to_unix(instance['timestamp'])
        # if instance['update_date']:
        #     instance['update_date'] = User.format_date_to_unix(instance['update_date'])

        return instance
