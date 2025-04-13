from payments.serializers import PaymentSerializer, TokenizedCardSerializer
from rest_framework.views import APIView
from payments.services import AdyenService
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from rest_framework import status

class CaptureInitialAuthView(APIView):
    """
    API endpoint to capture a pre-authorized payment.
    POST /api/v2/payments/capture/
    """
    async def post(self, request):
        serializer = TokenizedCardSerializer(data=request.data)
        if serializer.is_valid():
            try:
                tokenised_card = await sync_to_async(serializer.save)()
                service = AdyenService()
                result = await service.capture_initial_auth(tokenised_card)
                return Response(PaymentSerializer(result).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)