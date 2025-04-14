from django.conf import settings
import Adyen
import uuid
import asyncio
from asgiref.sync import sync_to_async
from decimal import Decimal
from payments.models import Payment, TokenizedCard, CardTokenRequest

class AdyenService:
    def __init__(self):
        self.adyen = Adyen.Adyen()
        self.adyen.payment.client.xapikey = settings.ADYEN_API_KEY
        self.adyen.payment.client.platform = "test" if settings.ADYEN_ENVIRONMENT == "Test" else "live"
        self.adyen.payment.client.merchant_account = settings.ADYEN_MERCHANT_ACCOUNT
        
    def get_ui_component_source(self):
        return settings.get_adyen_ui_component_source()  # Accesses the helper function defined in settings.py

    async def retrieve_token(self, card_token_request: CardTokenRequest) -> TokenizedCard:
        """
        Tokenizes a card, equivalent to .NET RetrieveToken(CardTokenRequest).
        Creates a TokenisedCard with a Payment, using Adyen's /payments API.
        Args:
            card_token_request (CardTokenRequest): Card details and customer info.
        Returns:
            TokenisedCard: Tokenized card details with associated Payment.
        """
        # Map CardTokenRequest to Adyen paymentMethod (like .NET CardDetails)
        payment_method = {
            "type": "scheme",
            "encryptedCardNumber": card_token_request.instrument,
            "encryptedExpiryMonth": str(card_token_request.expiry_month),
            "encryptedExpiryYear": str(card_token_request.expiry_year),
            "encryptedSecurityCode": card_token_request.cvv,
            "holderName": f"{card_token_request.card_holder_detail.first_name} {card_token_request.card_holder_detail.last_name}".strip()
        }

        # Build payment request (like .NET PaymentRequest)
        request = {
            "merchantAccount": settings.ADYEN_MERCHANT_ACCOUNT,
            "amount": {"value": 0, "currency": "AUD"},
            "reference": f"retrieveTokenBase_{uuid.uuid4()}",
            "returnUrl": "https://your-company.com/redirect",
            "paymentMethod": payment_method,
            "storePaymentMethod": True,
            "recurringProcessingModel": "CardOnFile",
            "shopperInteraction": "Ecommerce",
            "shopperReference": card_token_request.customer_code,
            "idempotency_key": str(uuid.uuid4())
        }

        # Make async payment request (like PaymentsAsync)
        try:
            response = await self.adyen.checkout.payments_api.payments_async(request)
        except Exception as e:
            raise Exception(f"Payment request failed: {str(e)}")

        # Handle response (like paymentResponse.ResultCode)
        if response.get("resultCode") == "Authorised":
            # Create Payment (like .NET Payment)
            payment = await sync_to_async(Payment.objects.create)(
                bank_transaction_id=response.get("pspReference", ""),
                amount=Decimal("0.00"),  # Matches .NET Amount.Value
                gateway_response_message=response.get("resultCode", ""),
                status=response.get("resultCode", ""),
                customer_code=card_token_request.customer_code
            )

            # Create TokenisedCard (like .NET return new TokenisedCard)
            tokenised_card = await sync_to_async(TokenizedCard.objects.create)(
                card_token_request=card_token_request,
                card_holder_detail=card_token_request.card_holder_detail,
                payment=payment,
                token=response.get("additionalData", {}).get("recurring.recurringDetailReference", ""),
                save_card_for_future=True,
                brand_type=response.get("paymentMethod", {}).get("brand", ""),
                customer_code=card_token_request.customer_code,
                merchant_reference=response.get("merchantReference", ""),
                scheme=response.get("paymentMethod", {}).get("type", "")
            )
            return tokenised_card

        raise Exception(response.get("refusalReason", "Tokenization failed"))

    async def create_payment(self, tokenised_card):
        """
        Processes a payment using a stored card, equivalent to .NET CreatePayment.
        Args:
            tokenised_card (TokenisedCard): Contains token and UIComponentRequest.
        Returns:
            Payment: Payment details with bank transaction ID and status.
        """
        # Map to Adyen paymentMethod (like .NET CardDetails)
        payment_method = {
            "type": "scheme",
            "storedPaymentMethodId": tokenised_card.token,
            "encryptedSecurityCode": "test_737"  # Hardcoded to match .NET
        }

        # Build payment request (like .NET PaymentRequest)
        request = {
            "merchantAccount": settings.ADYEN_MERCHANT_ACCOUNT,
            "amount": {
                "value": int(tokenised_card.ui_component_request.amount_to_charge * 100),
                "currency": "AUD"
            },
            "reference": f"createPaymentBase_{uuid.uuid4()}",
            "returnUrl": "https://your-company.com/redirect",
            "paymentMethod": payment_method,
            "recurringProcessingModel": "CardOnFile",
            "shopperInteraction": "ContAuth",
            "shopperReference": tokenised_card.customer_code,
            "idempotency_key": str(uuid.uuid4())
        }

        # Make async payment request (like PaymentsAsync)
        try:
            response = await self.adyen.checkout.payments_api.payments_async(request)
        except Exception as e:
            raise Exception(f"Payment request failed: {str(e)}")

        # Handle response (like paymentResponse.ResultCode)
        if response.get("resultCode") == "Authorised":
            # Create Payment (like .NET Payment)
            payment = await sync_to_async(Payment.objects.create)(
                bank_transaction_id=response.get("pspReference", ""),
                amount=tokenised_card.ui_component_request.amount_to_charge,
                gateway_response_message=response.get("resultCode", ""),
                status=response.get("resultCode", ""),
                customer_code=tokenised_card.customer_code
            )
            return payment

        raise Exception(response.get("refusalReason", "Payment failed"))

    async def refund_payment(self, ui_component_request):
        """
        Refunds a captured payment, equivalent to .NET RefundPayment.
        Args:
            ui_component_request (UIComponentRequest): Contains amount and order ID.
        Returns:
            Payment: Refund details with bank transaction ID and status.
        """
        # Build refund request (like .NET PaymentRefundRequest)
        request = {
            "merchantAccount": settings.ADYEN_MERCHANT_ACCOUNT,
            "amount": {
                "value": int(ui_component_request.amount_to_charge * 100),
                "currency": "AUD"
            },
            "reference": f"refundPaymentBase_{uuid.uuid4()}",
            "paymentPspReference": ui_component_request.order_id
        }

        # Make async refund request (like RefundCapturedPaymentAsync)
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.adyen.checkout.payments_api.payment_refund(request)
            )
        except Exception as e:
            raise Exception(f"Refund request failed: {str(e)}")

        # Handle response (like paymentRefundResponse.Status)
        if response.get("status") == "Received":
            # Create Payment (like .NET Payment)
            payment = await sync_to_async(Payment.objects.create)(
                bank_transaction_id=response.get("pspReference", ""),
                amount=ui_component_request.amount_to_charge,
                status=response.get("status", ""),
                gateway_response_message=response.get("status", ""),
                customer_code=ui_component_request.customer_code
            )
            return payment

        raise Exception(response.get("message", "Refund failed"))

    async def delete_payment_instrument(self, ui_component_request, token_to_delete):
        """
        Deletes a stored payment method, equivalent to .NET DeletePaymentInstrument.
        Args:
            ui_component_request (UIComponentRequest): Contains customer code.
            token_to_delete (str): The stored payment method ID to delete.
        Returns:
            bool: True if deletion is successful.
        """
        # Build delete request (like .NET DeleteTokenForStoredPaymentDetailsAsync)
        request = {
            "merchantAccount": settings.ADYEN_MERCHANT_ACCOUNT,
            "shopperReference": ui_component_request.customer_code,
            "recurringDetailReference": token_to_delete
        }

        # Make async delete request
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.adyen.recurring.disable_stored_payment_details(request)
            )
        except Exception as e:
            raise Exception(f"Delete token request failed: {str(e)}")

        # Assume success if no exception (like .NET returning true)
        return True

    async def create_initial_auth(self, tokenised_card):
        """
        Creates a pre-authorization payment, equivalent to .NET CreateInitialAuth.
        Args:
            tokenised_card (TokenisedCard): Contains token and UIComponentRequest.
        Returns:
            Payment: Pre-auth details with bank transaction ID and status.
        """
        # Map to Adyen paymentMethod (like .NET CardDetails)
        payment_method = {
            "type": "scheme",
            "storedPaymentMethodId": tokenised_card.token,
            "encryptedSecurityCode": "test_737"
        }

        # Build payment request (like .NET PaymentRequest)
        request = {
            "merchantAccount": settings.ADYEN_MERCHANT_ACCOUNT,
            "amount": {
                "value": int(tokenised_card.ui_component_request.amount_to_charge * 100),
                "currency": "AUD"
            },
            "reference": f"createInitialAuthBase_{uuid.uuid4()}",
            "returnUrl": "https://your-company.com/redirect",
            "paymentMethod": payment_method,
            "recurringProcessingModel": "CardOnFile",
            "shopperInteraction": "ContAuth",
            "shopperReference": tokenised_card.customer_code,
            "additionalData": {
                "authorisationType": "PreAuth",
                "manualCapture": "true"
            }
        }

        # Make async payment request (like PaymentsAsync)
        try:
            response = await self.adyen.checkout.payments_api.payments_async(request)
        except Exception as e:
            raise Exception(f"Payment request failed: {str(e)}")

        # Handle response (like paymentResponse.ResultCode)
        if response.get("resultCode") == "Authorised":
            # Create Payment (like .NET Payment)
            payment = await sync_to_async(Payment.objects.create)(
                bank_transaction_id=response.get("pspReference", ""),
                is_init_auth=True,
                status=response.get("resultCode", ""),
                gateway_response_message=response.get("resultCode", ""),
                customer_code=tokenised_card.customer_code,
                amount=tokenised_card.ui_component_request.amount_to_charge
            )
            return payment

        raise Exception(response.get("refusalReason", "Pre-authorization failed"))

    async def cancel_initial_auth(self, tokenised_card):
        """
        Cancels a pre-authorized payment, equivalent to .NET CancelInitialAuth.
        Args:
            tokenised_card (TokenisedCard): Contains UIComponentRequest with OrderID.
        Returns:
            Payment: Cancellation details with bank transaction ID and status.
        """
        # Build cancel request (like .NET PaymentCancelRequest)
        request = {
            "merchantAccount": settings.ADYEN_MERCHANT_ACCOUNT,
            "reference": f"cancelInitialAuthBase_{uuid.uuid4()}",
            "paymentPspReference": tokenised_card.ui_component_request.order_id
        }

        # Make async cancel request (like CancelAuthorisedPaymentByPspReferenceAsync)
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.adyen.checkout.payment_cancel(request)
            )
        except Exception as e:
            raise Exception(f"Cancel request failed: {str(e)}")

        # Handle response (like createPaymentCancelResponse.Status)
        if response.get("status") == "Received":
            # Create Payment (like .NET Payment)
            payment = await sync_to_async(Payment.objects.create)(
                bank_transaction_id=response.get("pspReference", ""),
                order_id=response.get("paymentPspReference", ""),
                merchant_code=response.get("merchantAccount", ""),
                status=response.get("status", ""),
                customer_code=tokenised_card.customer_code
            )
            return payment

        raise Exception(response.get("message", "Cancel failed"))

    async def capture_initial_auth(self, tokenised_card):
        """
        Captures a pre-authorized payment, equivalent to .NET CaptureInitialAuth.
        Args:
            tokenised_card (TokenisedCard): Contains UIComponentRequest with OrderID and Amount.
        Returns:
            Payment: Capture details with bank transaction ID and status.
        """
        # Build capture request (like .NET PaymentCaptureRequest)
        request = {
            "merchantAccount": settings.ADYEN_MERCHANT_ACCOUNT,
            "amount": {
                "value": int(tokenised_card.ui_component_request.amount_to_charge * 100),
                "currency": "AUD"
            },
            "reference": f"captureInitialAuthBase_{uuid.uuid4()}",
            "paymentPspReference": tokenised_card.ui_component_request.order_id
        }

        # Make async capture request (like CaptureAuthorisedPaymentAsync)
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.adyen.checkout.payment_capture(request)
            )
        except Exception as e:
            raise Exception(f"Capture request failed: {str(e)}")

        # Handle response (like createPaymentCaptureResponse.Status)
        if response.get("status") == "Received":
            # Create Payment (like .NET Payment)
            payment = await sync_to_async(Payment.objects.create)(
                bank_transaction_id=response.get("pspReference", ""),
                order_id=response.get("paymentPspReference", ""),
                merchant_code=response.get("merchantAccount", ""),
                status=response.get("status", ""),
                customer_code=tokenised_card.customer_code,
                amount=tokenised_card.ui_component_request.amount_to_charge
            )
            return payment

        raise Exception(response.get("message", "Capture failed"))

    async def increase_initial_auth(self, tokenised_card):
        """
        Increases a pre-authorized amount, equivalent to .NET IncreaseInitialAuth.
        Args:
            tokenised_card (TokenisedCard): Contains UIComponentRequest with OrderID and Amount.
        Returns:
            Payment: Updated auth details with bank transaction ID and status.
        """
        # Build amount update request (like .NET PaymentAmountUpdateRequest)
        request = {
            "merchantAccount": settings.ADYEN_MERCHANT_ACCOUNT,
            "amount": {
                "value": int(tokenised_card.ui_component_request.amount_to_charge * 100),
                "currency": "AUD"
            },
            "reference": f"increaseInitialAuthBase_{uuid.uuid4()}",
            "paymentPspReference": tokenised_card.ui_component_request.order_id
        }

        # Make async amount update request (like UpdateAuthorisedAmountAsync)
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.adyen.checkout.payment_amount_updates(request)
            )
        except Exception as e:
            raise Exception(f"Amount update request failed: {str(e)}")

        # Handle response (like createPaymentAmountUpdateResponse.Status)
        if response.get("status") == "Received":
            # Create Payment (like .NET Payment)
            payment = await sync_to_async(Payment.objects.create)(
                bank_transaction_id=response.get("pspReference", ""),
                order_id=response.get("paymentPspReference", ""),
                status=response.get("status", ""),
                is_init_auth=True,
                customer_code=tokenised_card.customer_code,
                amount=tokenised_card.ui_component_request.amount_to_charge
            )
            return payment

        raise Exception(response.get("message", "Amount update failed"))