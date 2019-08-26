from rest_framework import serializers
from .models import Car
from client.models import User


class CarListSerializer(serializers.ModelSerializer):  # Список всех машин
    class Meta:
        model = Car
        fields = ('id', 'reg_num', 'user')

    def to_representation(self, data):
        instance = super(CarListSerializer, self).to_representation(data)

        instance['ok'] = True
        if instance['timestamp']:
            instance['timestamp'] = User.format_date_to_unix(instance['timestamp'])
        if instance['update_date']:
            instance['update_date'] = User.format_date_to_unix(instance['update_date'])

        return instance


class CarDetailSerializer(serializers.ModelSerializer):  # Добавление машины
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Прячем пользователя, чтобы не поменяли

    class Meta:
        model = Car
        fields = ('id', 'reg_num', 'user', 'timestamp', 'update_date')

    def to_representation(self, data):
        instance = super(CarDetailSerializer, self).to_representation(data)

        instance['ok'] = True
        if instance['timestamp']:
            instance['timestamp'] = User.format_date_to_unix(instance['timestamp'])
        if instance['update_date']:
            instance['update_date'] = User.format_date_to_unix(instance['update_date'])

        return instance
