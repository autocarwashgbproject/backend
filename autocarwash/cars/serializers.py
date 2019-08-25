from rest_framework import serializers
from cars.models import Car


class CarsListSerializer(serializers.ModelSerializer):  # Список всех машин
    class Meta:
        model = Car
        fields = ('id', 'reg_num', 'user')


class CarDetailSerializer(serializers.ModelSerializer):  # Добавление машины
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Прячем пользователя, чтобы не поменяли

    class Meta:
        model = Car
        fields = '__all__'
