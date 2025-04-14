from payments.serializers import CardTokenRequestSerializer, TokenizedCardSerializer
from rest_framework.views import APIView
from payments.services import AdyenService
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from rest_framework import status

class RetrieveTokenView(APIView):
    """
    API endpoint to tokenize a card.
    POST /api/v2/payment-instruments/tokenise/
    """
    async def post(self, request):
        serializer = CardTokenRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                card_token_request = await sync_to_async(serializer.save)()
                service = AdyenService()
                tokenized_card = await service.retrieve_token(card_token_request)
                serialized_card = TokenizedCardSerializer(tokenized_card)
                return Response(serialized_card.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
