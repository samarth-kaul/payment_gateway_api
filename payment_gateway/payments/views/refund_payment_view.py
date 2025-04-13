from payments.serializers import UIComponentRequestSerializer, PaymentSerializer
from rest_framework.views import APIView
from payments.services import AdyenService
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from rest_framework import status

class RefundPaymentView(APIView):
    """
    API endpoint to refund a captured payment.
    POST /api/v2/payments/refund/
    """
    async def post(self, request):
        serializer = UIComponentRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                ui_component_request = await sync_to_async(serializer.save)()
                service = AdyenService()
                result = await service.refund_payment(ui_component_request)
                return Response(PaymentSerializer(result).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)