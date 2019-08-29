from rest_framework import serializers
from .models import Washing
from client.models import User

class CreateWashingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Washing
        fields = "__all__"

    def to_representation(self, data):
        instance = super(CreateWashingSerializer, self).to_representation(data)

        instance['timestamp'] = User.format_date_to_unix(instance['timestamp'])

        return instance
