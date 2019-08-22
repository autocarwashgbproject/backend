from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    # created_by = serializers.ReadOnlyField(source='created_by.username')
    # reviews = ReviewSerializer(many=True, read_only=True)


    class Meta:
        model = User
        fields = ('id', 'phone', 'name', 'surname', 'patronymic', 'email', 'birthday', 'timestamp', 'update_date', )

    def to_representation(self, data):
        instance = super(UserDetailSerializer, self).to_representation(data)

        instance['phone'] = int(instance['phone'])
        instance['ok'] = True
        if instance['birthday']:
            instance['birthday'] = User.format_date_to_unix(instance['birthday'])
        if instance['timestamp']:
            instance['timestamp'] = User.format_date_to_unix(instance['timestamp'])
        if instance['update_date']:
            instance['update_date'] = User.format_date_to_unix(instance['update_date'])


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
            instance = super(UserDetailSerializer, self).to_representation(data)

            instance['phone'] = int(instance['phone'])
            instance['ok'] = True

            return instance
