# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .services import AdyenService
# from .serializers import (
#     CardTokenRequestSerializer,
#     TokenizedCardSerializer,
#     PaymentSerializer,
#     UIComponentRequestSerializer
# )
# from asgiref.sync import sync_to_async


# class RetrieveTokenView(APIView):
#     """
#     API endpoint to tokenize a card.
#     POST /api/v2/payment-instruments/tokenise/
#     """
#     async def post(self, request):
#         serializer = CardTokenRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 card_token_request = await sync_to_async(serializer.save)()
#                 service = AdyenService()
#                 result = await service.retrieve_token(card_token_request)
#                 return Response(TokenizedCardSerializer(result).data, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CreatePaymentView(APIView):
#     """
#     API endpoint to process a payment using a stored card.
#     POST /api/v2/payments/
#     """
#     async def post(self, request):
#         serializer = TokenizedCardSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 tokenised_card = await sync_to_async(serializer.save)()
#                 service = AdyenService()
#                 result = await service.create_payment(tokenised_card)
#                 return Response(PaymentSerializer(result).data, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RefundPaymentView(APIView):
#     """
#     API endpoint to refund a captured payment.
#     POST /api/v2/payments/refund/
#     """
#     async def post(self, request):
#         serializer = UIComponentRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 ui_component_request = await sync_to_async(serializer.save)()
#                 service = AdyenService()
#                 result = await service.refund_payment(ui_component_request)
#                 return Response(PaymentSerializer(result).data, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DeletePaymentInstrumentView(APIView):
#     """
#     API endpoint to delete a stored payment method.
#     POST /api/v2/payment-instruments/delete/
#     """
#     async def post(self, request):
#         serializer = UIComponentRequestSerializer(data=request.data)
#         token_to_delete = request.data.get("token_to_delete")
#         if serializer.is_valid() and token_to_delete:
#             try:
#                 ui_component_request = await sync_to_async(serializer.save)()
#                 service = AdyenService()
#                 result = await service.delete_payment_instrument(ui_component_request, token_to_delete)
#                 return Response({"success": result}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


# class CreateInitialAuthView(APIView):
#     """
#     API endpoint to create a pre-authorization payment.
#     POST /api/v2/payments/initial-auth/
#     """
#     async def post(self, request):
#         serializer = TokenizedCardSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 tokenised_card = await sync_to_async(serializer.save)()
#                 service = AdyenService()
#                 result = await service.create_initial_auth(tokenised_card)
#                 return Response(PaymentSerializer(result).data, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CancelInitialAuthView(APIView):
#     """
#     API endpoint to cancel a pre-authorized payment.
#     POST /api/v2/payments/cancel/
#     """
#     async def post(self, request):
#         serializer = TokenizedCardSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 tokenised_card = await sync_to_async(serializer.save)()
#                 service = AdyenService()
#                 result = await service.cancel_initial_auth(tokenised_card)
#                 return Response(PaymentSerializer(result).data, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CaptureInitialAuthView(APIView):
#     """
#     API endpoint to capture a pre-authorized payment.
#     POST /api/v2/payments/capture/
#     """
#     async def post(self, request):
#         serializer = TokenizedCardSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 tokenised_card = await sync_to_async(serializer.save)()
#                 service = AdyenService()
#                 result = await service.capture_initial_auth(tokenised_card)
#                 return Response(PaymentSerializer(result).data, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class IncreaseInitialAuthView(APIView):
#     """
#     API endpoint to increase a pre-authorized payment amount.
#     POST /api/v2/payments/increase-auth/
#     """
#     async def post(self, request):
#         serializer = TokenizedCardSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 tokenised_card = await sync_to_async(serializer.save)()
#                 service = AdyenService()
#                 result = await service.increase_initial_auth(tokenised_card)
#                 return Response(PaymentSerializer(result).data, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)