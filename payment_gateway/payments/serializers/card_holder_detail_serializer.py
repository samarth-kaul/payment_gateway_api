from rest_framework import serializers
from payments.models import CardHolderDetail

class CardHolderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardHolderDetail
        fields = '__all__'
