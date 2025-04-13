from rest_framework import serializers
from payments.serializers import UIComponentRequestSerializer, CardHolderDetailSerializer, PaymentSerializer, CardTokenRequestSerializer
from payments.models import CardHolderDetail, CardTokenRequest, UIComponentRequest, TokenizedCard

class TokenizedCardSerializer(serializers.ModelSerializer):
    card_holder_detail = CardHolderDetailSerializer(required=False, allow_null=True)
    payment = PaymentSerializer(required=False, allow_null=True)
    card_token_request = CardTokenRequestSerializer(required=False, allow_null=True)
    ui_component_request = UIComponentRequestSerializer(required=False, allow_null=True)
    pan = serializers.ReadOnlyField()
    expiry_date = serializers.ReadOnlyField()
    card_type = serializers.ReadOnlyField()
    
    
    class Meta:
        model = TokenizedCard
        fields = '__all__'

    def create(self, validated_data):
        card_token_data = validated_data.pop("card_token_request")
        card_holder_data = validated_data.pop("card_holder_detail")
        ui_component_data = validated_data.pop("ui_component_request")
        card_holder = CardHolderDetail.objects.create(**card_holder_data)
        card_token = CardTokenRequest.objects.create(
            card_holder_detail=card_holder, **card_token_data
        )
        ui_component = UIComponentRequest.objects.create(**ui_component_data)
        return TokenizedCard.objects.create(
            card_token_request=card_token,
            card_holder_detail=card_holder,
            ui_component_request=ui_component,
            **validated_data
        )





