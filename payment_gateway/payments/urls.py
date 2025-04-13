# from django.urls import path
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .views import (
#     CreatePaymentInstrumentView, CreatePaymentView, RefundPaymentView,
#     CreateInitialAuthView, IncreaseInitialAuthView, CancelInitialAuthView,
#     CaptureInitialAuthView, GetPaymentInstrumentsView, DeletePaymentInstrumentView,
#     RetrievePublicKeyView, RetrieveTokenView, AccountVerificationView
# )

# @api_view(['GET'])
# def api_root(request):
#     return Response({"message": "Welcome to Payments API v2"})

# urlpatterns = [
#     path('', api_root, name='api_root'),
#     path('customers/<str:customer_code>/payment-instruments/token/', CreatePaymentInstrumentView.as_view(), name='create_payment_instrument'),
#     path('payments/', CreatePaymentView.as_view(), name='create_payment'),
#     path('orders/<str:order_id>/refunds/', RefundPaymentView.as_view(), name='refund_payment'),
#     path('payments/account-verification/', AccountVerificationView.as_view(), name='account_verification'),
#     path('payments/preauths/', CreateInitialAuthView.as_view(), name='create_initial_auth'),
#     path('payments/preauths/<str:order_id>/increase/', IncreaseInitialAuthView.as_view(), name='increase_initial_auth'),
#     path('payments/preauths/<str:order_id>/cancel/', CancelInitialAuthView.as_view(), name='cancel_initial_auth'),
#     path('payments/preauths/<str:order_id>/capture/', CaptureInitialAuthView.as_view(), name='capture_initial_auth'),
#     path('customers/<str:customer_code>/payment-instruments/', GetPaymentInstrumentsView.as_view(), name='get_payment_instruments'),
#     path('customers/<str:customer_code>/payment-instruments/<str:token>/', DeletePaymentInstrumentView.as_view(), name='delete_payment_instrument'),
#     path('clients/<str:client_id>/ui/config/', RetrievePublicKeyView.as_view(), name='retrieve_public_key'),
#     path('payment-instruments/tokenise/', RetrieveTokenView.as_view(), name='retrieve_token'),
# ]

from django.urls import path
from payments.views import(
    RetrieveTokenView,
    CreatePaymentView,
    RefundPaymentView,
    DeletePaymentInstrumentView,
    CreateInitialAuthView,
    CancelInitialAuthView,
    CaptureInitialAuthView,
    IncreaseInitialAuthView
)

urlpatterns = [
    path('payment-instruments/tokenise/', RetrieveTokenView.as_view(), name='retrieve-token'),
    path('payments/', CreatePaymentView.as_view(), name='create-payment'),
    path('payments/refund/', RefundPaymentView.as_view(), name='refund-payment'),
    path('payment-instruments/delete/', DeletePaymentInstrumentView.as_view(), name='delete-payment-instrument'),
    path('payments/initial-auth/', CreateInitialAuthView.as_view(), name='create-initial-auth'),
    path('payments/cancel/', CancelInitialAuthView.as_view(), name='cancel-initial-auth'),
    path('payments/capture/', CaptureInitialAuthView.as_view(), name='capture-initial-auth'),
    path('payments/increase-auth/', IncreaseInitialAuthView.as_view(), name='increase-initial-auth'),
]