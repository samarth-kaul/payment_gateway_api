# from rest_framework import serializers
# from .models import (
#     CardHolderDetail, CardTokenRequest, Payment, PaymentInstrument,
#     UIComponentRequest, FraudCheckResult, TokenisedCard
# )

# class CardHolderDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CardHolderDetail
#         fields = [
#             'frequent_flyer_number', 'ref_title', 'title', 'first_name', 'last_name',
#             'email', 'is_required_tax_invoice', 'is_default'
#         ]

# class CardTokenRequestSerializer(serializers.ModelSerializer):
#     card_holder_detail = CardHolderDetailSerializer()

#     class Meta:
#         model = CardTokenRequest
#         fields = [
#             'card_holder_detail', 'instrument', 'cvv', 'expiry_month', 'expiry_year',
#             'scheme', 'save_for_future', 'customer_code'
#         ]

#     def create(self, validated_data):
#         card_holder_data = validated_data.pop('card_holder_detail')
#         card_holder = CardHolderDetail.objects.create(**card_holder_data)
#         card_token_request = CardTokenRequest.objects.create(
#             card_holder_detail=card_holder, **validated_data
#         )
#         return card_token_request

# class FraudCheckResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FraudCheckResult
#         fields = ['provider_reference_number', 'score', 'provider_response_message']

# class PaymentSerializer(serializers.ModelSerializer):
#     bank_transaction_id = serializers.CharField(source='bank_transaction_id')
#     is_init_auth = serializers.BooleanField(source='is_init_auth')
#     fraud_check_result = FraudCheckResultSerializer()

#     class Meta:
#         model = Payment
#         fields = [
#             'is_init_auth', 'created_at', 'merchant_code', 'customer_code', 'token',
#             'ip', 'amount', 'status', 'order_id', 'bank_transaction_id',
#             'gateway_response_code', 'gateway_response_message', 'error_code',
#             'fraud_check_type', 'fraud_check_result'
#         ]

# class PaymentInstrumentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentInstrument
#         fields = [
#             'created_at', 'customer_code', 'brand_type', 'brand_category', 'token',
#             'scheme', 'last4', 'expiry_month', 'expiry_year'
#         ]

# class PaymentInstrumentListSerializer(serializers.Serializer):
#     payment_instruments = PaymentInstrumentSerializer(many=True)

# class UIComponentRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UIComponentRequest
#         fields = [
#             'merchant_code', 'client_id', 'customer_code', 'order_id', 'idempotency_key',
#             'amount_to_charge', 'client_ip', 'required_card_holder_detail',
#             'transaction_type', 'ui_component_string'
#         ]

# class TokenisedCardSerializer(serializers.ModelSerializer):
#     ui_component_request = UIComponentRequestSerializer()
#     card_holder_detail = CardHolderDetailSerializer()
#     payment = PaymentSerializer()
#     card_token_request = CardTokenRequestSerializer()
#     pan = serializers.ReadOnlyField()
#     expiry_date = serializers.ReadOnlyField()
#     card_type = serializers.ReadOnlyField()

#     class Meta:
#         model = TokenisedCard
#         fields = [
#             'ui_component_request', 'card_holder_detail', 'payment', 'card_token_request',
#             'merchant_code', 'token', 'created_at', 'scheme', 'bin', 'last4',
#             'expiry_month', 'expiry_year', 'customer_code', 'brand_type',
#             'brand_category', 'merchant_reference', 'save_card_for_future',
#             'deleted', 'is_new', 'pan', 'expiry_date', 'card_type'
#         ]