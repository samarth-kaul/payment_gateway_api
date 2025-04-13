from rest_framework import serializers
from payments.models.payment import Payment
from payments.serializers import FraudCheckResultSerializer

class PaymentSerializer(serializers.ModelSerializer):
    fraud_check_result = FraudCheckResultSerializer(required=False, allow_null=True)

    class Meta:
        model = Payment
        fields = '__all__'
