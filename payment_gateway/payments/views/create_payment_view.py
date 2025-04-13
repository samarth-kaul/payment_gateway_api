from payments.serializers import PaymentSerializer, TokenizedCardSerializer
from rest_framework.views import APIView
from payments.services import AdyenService
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from rest_framework import status

class CreatePaymentView(APIView):
    """
    API endpoint to process a payment using a stored card.
    POST /api/v2/payments/
    """
    def post(self, request):
        serializer = TokenizedCardSerializer(data=request.data)
        if serializer.is_valid():
            try:
                tokenised_card = serializer.save()
                service = AdyenService()
                result = service.create_payment(tokenised_card)
                return Response(PaymentSerializer(result).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
