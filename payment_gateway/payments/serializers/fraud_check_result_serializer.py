from rest_framework import serializers
from payments.models import FraudCheckResult

class FraudCheckResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudCheckResult
        fields = '__all__'
