from payments.serializers import PaymentSerializer, TokenizedCardSerializer
from rest_framework.views import APIView
from payments.services import AdyenService
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from rest_framework import status

class IncreaseInitialAuthView(APIView):
    """
    API endpoint to increase a pre-authorized payment amount.
    POST /api/v2/payments/increase-auth/
    """
    def post(self, request):
        serializer = TokenizedCardSerializer(data=request.data)
        if serializer.is_valid():
            try:
                tokenised_card =  serializer.save()
                service = AdyenService()
                result = service.increase_initial_auth(tokenised_card)
                return Response(PaymentSerializer(result).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)