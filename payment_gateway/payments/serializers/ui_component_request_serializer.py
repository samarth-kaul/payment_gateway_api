from rest_framework import serializers
from payments.models import UIComponentRequest

class UIComponentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UIComponentRequest
        fields = '__all__'