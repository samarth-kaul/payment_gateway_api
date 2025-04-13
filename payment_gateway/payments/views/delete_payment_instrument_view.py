from payments.serializers import UIComponentRequestSerializer
from rest_framework.views import APIView
from payments.services import AdyenService
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from rest_framework import status

class DeletePaymentInstrumentView(APIView):
    """
    API endpoint to delete a stored payment method.
    POST /api/v2/payment-instruments/delete/
    """
    def post(self, request):
        serializer = UIComponentRequestSerializer(data=request.data)
        token_to_delete = request.data.get("token_to_delete")
        if serializer.is_valid() and token_to_delete:
            try:
                ui_component_request =  serializer.save()
                service = AdyenService()
                result = service.delete_payment_instrument(ui_component_request, token_to_delete)
                return Response({"success": result}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
