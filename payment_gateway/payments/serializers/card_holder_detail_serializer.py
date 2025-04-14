from rest_framework import serializers
from payments.models import CardHolderDetail

# class CardHolderDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CardHolderDetail
#         fields = '__all__'


class CardHolderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardHolderDetail
        fields = [
            'frequent_flyer_number',
            'ref_title',
            'title',
            'first_name',
            'last_name',
            'email',
            'is_required_tax_invoice',
            'is_default'
        ]