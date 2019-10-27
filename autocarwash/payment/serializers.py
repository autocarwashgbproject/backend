from rest_framework import serializers
from .models import OrderBankUsers, BankUsers, CardBankUsers
from client.models import User

class ViewPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderBankUsers
        fields = ('card_bank_users', 'car', 'subscription', 'is_paid', 'error', 'error_description', 'refundable', 'status', 'created_at')

    def to_representation(self, data):
        instance = super(ViewPaymentSerializer, self).to_representation(data)

        instance['created_at'] = User.format_date_to_unix(instance['created_at'])

        return instance


class ViewCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardBankUsers
        fields = ('id', 'timestamp', 'last4', 'card_type', 'bank')

    def to_representation(self, data):
        instance = super(ViewCardsSerializer, self).to_representation(data)

        instance['timestamp'] = User.format_date_to_unix(instance['timestamp'])

        return instance
