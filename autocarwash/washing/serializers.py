from rest_framework import serializers
from .models import Washing

class CreateWashingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Washing
        fields = "__all__"# ('', '', )
