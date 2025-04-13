from rest_framework import serializers
from payments.models.card_token_request import CardTokenRequest, CardHolderDetail
from payments.serializers import CardHolderDetailSerializer

class CardTokenRequestSerializer(serializers.ModelSerializer):
    card_holder_detail = CardHolderDetailSerializer()

    class Meta:
        model = CardTokenRequest
        fields = '__all__'

    def create(self, validated_data):
        card_holder_data = validated_data.pop("card_holder_detail")
        card_holder = CardHolderDetail.objects.create(**card_holder_data)
        return CardTokenRequest.objects.create(
            card_holder_detail=card_holder, **validated_data
        )
