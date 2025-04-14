from rest_framework import serializers
from payments.models import Payment, FraudCheckResult
from payments.serializers import FraudCheckResultSerializer

# class PaymentSerializer(serializers.ModelSerializer):
#     fraud_check_result = FraudCheckResultSerializer(required=False, allow_null=True)

#     class Meta:
#         model = Payment
#         fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    fraud_check_result = FraudCheckResultSerializer(allow_null=True)
    class Meta:
        model = Payment
        fields = [
            'is_init_auth',
            'created_at',
            'merchant_code',
            'customer_code',
            'token',
            'ip',
            'amount',
            'status',
            'order_id',
            'bank_transaction_id',
            'gateway_response_code',
            'gateway_response_message',
            'error_code',
            'fraud_check_type',
            'fraud_check_result'
        ]

    def create(self, validated_data):
        fraud_check_data = validated_data.pop('fraud_check_result', None)
        if fraud_check_data:
            fraud_check_result = FraudCheckResult.objects.create(**fraud_check_data)
            validated_data['fraud_check_result'] = fraud_check_result
        return Payment.objects.create(**validated_data)


