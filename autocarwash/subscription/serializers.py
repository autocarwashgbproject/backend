from rest_framework import serializers
from .models import Subscription


class SubscriptionListSerializer(serializers.ModelSerializer):  # Список всех машин
    class Meta:
        model = Subscription
        fields = ('id', 'city', 'subscription', )

    def to_representation(self, data):
        instance = super(SubscriptionListSerializer, self).to_representation(data)

        instance['subscription_price'] = Subscription.subscription_price()

        return instance
