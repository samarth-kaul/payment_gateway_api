from rest_framework import serializers
from payments.models import FraudCheckResult

# class FraudCheckResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FraudCheckResult
#         fields = '__all__'

class FraudCheckResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudCheckResult
        fields = [
            'provider_reference_number',
            'score',
            'provider_response_message'
        ]