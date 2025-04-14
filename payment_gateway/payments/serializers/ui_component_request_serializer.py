from rest_framework import serializers
from payments.models import UIComponentRequest

# class UIComponentRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UIComponentRequest
#         fields = '__all__'

class UIComponentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UIComponentRequest
        fields = [
            'merchant_code',
            'client_id',
            'customer_code',
            'order_id',
            'idempotency_key',
            'amount_to_charge',
            'client_ip',
            'required_card_holder_detail',
            'transaction_type',
            'ui_component_string'
        ]
