from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from car.models import Car
from payment.models import BankUsers

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    # created_by = serializers.ReadOnlyField(source='created_by.username')
    # reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'phone', 'name', 'surname', 'patronymic', 'email', 'birthday', 'timestamp', 'update_date', )

    def to_representation(self, data):
        instance = super(UserDetailSerializer, self).to_representation(data)

        instance['phone'] = instance['phone']
        instance['ok'] = True
        if instance['birthday']:
            instance['birthday'] = User.format_date_to_unix(instance['birthday'])
            instance['is_birthday'] = True
        else:
            instance['is_birthday'] = False
        if instance['timestamp']:
            instance['timestamp'] = User.format_date_to_unix(instance['timestamp'])
        if instance['update_date']:
            instance['update_date'] = User.format_date_to_unix(instance['update_date'])

        cars = Car.objects.filter(user = instance['id'])
        cars_id = []
        if cars.exists():
            cars_id = [car.id for car in cars]

        instance['cars_id'] = cars_id

        bankusers = BankUsers.objects.filter(user = instance['id'])
        bankusers_id = []
        if bankusers.exists():
            bankusers_id = [bankuser.id for bankuser in bankusers]
            print(bankusers_id)

        instance['user_card_id'] = bankusers_id

        return instance


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    def to_representation(self, data):
        instance = super(CreateUserSerializer, self).to_representation(data)

        instance['phone'] = instance['phone']
        instance['ok'] = True


        return instance
