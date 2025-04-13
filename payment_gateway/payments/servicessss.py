# import Adyen
# from django.conf import settings
# from .models import (
#     CardTokenRequest, Payment, PaymentInstrument, TokenisedCard, UIComponentRequest
# )
# import uuid

# class PaymentService:
#     def create_payment_instrument(self, card_token_request):
#         raise NotImplementedError

#     def create_payment(self, tokenised_card):
#         raise NotImplementedError

#     def refund_payment(self, tokenised_card):
#         raise NotImplementedError

#     def create_initial_auth(self, tokenised_card):
#         raise NotImplementedError

#     def increase_initial_auth(self, tokenised_card):
#         raise NotImplementedError

#     def cancel_initial_auth(self, tokenised_card):
#         raise NotImplementedError

#     def capture_initial_auth(self, tokenised_card):
#         raise NotImplementedError

#     def get_payment_instruments(self, customer_code):
#         raise NotImplementedError

#     def delete_payment_instrument(self, customer_code, token):
#         raise NotImplementedError

#     def retrieve_public_key(self, client_id):
#         raise NotImplementedError

#     def retrieve_token(self, card_token_request):
#         raise NotImplementedError

#     def account_verification(self, tokenised_card):
#         raise NotImplementedError

# class AdyenService(PaymentService):
#     def __init__(self):
#         self.adyen = Adyen.Adyen()
#         self.adyen.payment.client.api_key = settings.ADYEN_API_KEY
#         self.adyen.payment.client.platform = "test" if settings.ADYEN_ENVIRONMENT == "Test" else "live"
#         self.adyen.payment.client.merchant_account = settings.ADYEN_MERCHANT_ACCOUNT

#     def create_payment_instrument(self, card_token_request):
#         card_holder = card_token_request.card_holder_detail
#         card_data = {
#             'number': card_token_request.instrument,
#             'expiryMonth': str(card_token_request.expiry_month),
#             'expiryYear': str(card_token_request.expiry_year),
#             'cvc': card_token_request.cvv,
#             'holderName': f"{card_holder.first_name} {card_holder.last_name}".strip()
#         }
#         payment_request = {
#             'merchantAccount': settings.ADYEN_MERCHANT_ACCOUNT,
#             'amount': {'value': 0, 'currency': 'AUD'},
#             'reference': f"token_{uuid.uuid4()}",
#             'paymentMethod': card_data,
#             'storePaymentMethod': card_token_request.save_for_future,
#             'shopperReference': card_token_request.customer_code,
#             'shopperInteraction': 'Ecommerce',
#             'recurringProcessingModel': 'CardOnFile',
#             'returnUrl': 'https://your-company.com/redirect'
#         }
#         response = self.adyen.checkout.payments(payment_request)

#         if response.message.get('resultCode') == 'Authorised':
#             token = response.message['additionalData']['recurring.recurringDetailReference']
#             payment_instrument = PaymentInstrument.objects.create(
#                 customer_code=card_token_request.customer_code,
#                 token=token,
#                 last4=card_data['number'][-4:],
#                 scheme=response.message.get('paymentMethod', {}).get('type', ''),
#                 expiry_month=str(card_token_request.expiry_month).zfill(2),
#                 expiry_year=str(card_token_request.expiry_year),
#                 brand_type=response.message.get('paymentMethod', {}).get('brand', ''),
#                 brand_category=response.message.get('paymentMethod', {}).get('brand', '')
#             )
#             return payment_instrument
#         raise Exception(response.message.get('refusalReason', 'Tokenization failed'))

#     def create_payment(self, tokenised_card):
#         ui_component = tokenised_card.ui_component_request
#         payment_request = {
#             'merchantAccount': settings.ADYEN_MERCHANT_ACCOUNT,
#             'amount': {'value': int(ui_component.amount_to_charge * 100), 'currency': 'AUD'},
#             'reference': ui_component.idempotency_key or f"pay_{uuid.uuid4()}",
#             'paymentMethod': {
#                 'type': 'scheme',
#                 'storedPaymentMethodId': tokenised_card.token,
#                 'encryptedSecurityCode': 'test_737'
#             },
#             'shopperReference': ui_component.customer_code,
#             'shopperInteraction': 'ContAuth',
#             'recurringProcessingModel': 'CardOnFile',
#             'returnUrl': 'https://your-company.com/redirect',
#             'shopperIP': ui_component.client_ip
#         }
#         response = self.adyen.checkout.payments(payment_request)

#         if response.message.get('resultCode') in ['Authorised', 'Pending']:
#             payment = Payment.objects.create(
#                 bank_transaction_id=response.message['pspReference'],
#                 amount=ui_component.amount_to_charge,
#                 currency='AUD',
#                 status=response.message['resultCode'],
#                 merchant_code=ui_component.merchant_code or settings.ADYEN_MERCHANT_ACCOUNT,
#                 customer_code=ui_component.customer_code,
#                 token=tokenised_card.token,
#                 ip=ui_component.client_ip,
#                 order_id=ui_component.order_id or response.message['pspReference'],
#                 gateway_response_message=response.message.get('resultCode', '')
#             )
#             tokenised_card.payment = payment
#             tokenised_card.save()
#             return payment
#         raise Exception(response.message.get('refusalReason', 'Payment failed'))

#     def refund_payment(self, tokenised_card):
#         ui_component = tokenised_card.ui_component_request
#         payment = Payment.objects.get(order_id=ui_component.order_id)
#         refund_request = {
#             'merchantAccount': settings.ADYEN_MERCHANT_ACCOUNT,
#             'originalReference': payment.bank_transaction_id,
#             'amount': {'value': int(ui_component.amount_to_charge * 100), 'currency': 'AUD'},
#             'reference': ui_component.idempotency_key or f"refund_{uuid.uuid4()}"
#         }
#         response = self.adyen.checkout.refunds(refund_request)

#         if response.message.get('status') == 'received':
#             payment.status = 'Refunded'
#             payment.save()
#             refund_payment = Payment.objects.create(
#                 bank_transaction_id=response.message['pspReference'],
#                 amount=ui_component.amount_to_charge,
#                 currency='AUD',
#                 status='Refunded',
#                 merchant_code=ui_component.merchant_code or settings.ADYEN_MERCHANT_ACCOUNT,
#                 customer_code=ui_component.customer_code,
#                 gateway_response_message='Refunded'
#             )
#             return refund_payment
#         raise Exception('Refund failed')

#     def create_initial_auth(self, tokenised_card):
#         ui_component = tokenised_card.ui_component_request
#         payment_request = {
#             'merchantAccount': settings.ADYEN_MERCHANT_ACCOUNT,
#             'amount': {'value': int(ui_component.amount_to_charge * 100), 'currency': 'AUD'},
#             'reference': ui_component.idempotency_key or f"preauth_{uuid.uuid4()}",
#             'paymentMethod': {
#                 'type': 'scheme',
#                 'storedPaymentMethodId': tokenised_card.token,
#                 'encryptedSecurityCode': 'test_737'
#             },
#             'shopperReference': ui_component.customer_code,
#             'shopperInteraction': 'ContAuth',
#             'recurringProcessingModel': 'CardOnFile',
#             'returnUrl': 'https://your-company.com/redirect',
#             'shopperIP': ui_component.client_ip,
#             'additionalData': {
#                 'authorisationType': 'PreAuth',
#                 'manualCapture': 'true'
#             }
#         }
#         response = self.adyen.checkout.payments(payment_request)

#         if response.message.get('resultCode') == 'Authorised':
#             payment = Payment.objects.create(
#                 bank_transaction_id=response.message['pspReference'],
#                 amount=ui_component.amount_to_charge,
#                 currency='AUD',
#                 status=response.message['resultCode'],
#                 is_init_aut=True,
#                 merchant_code=ui_component.merchant_code or settings.ADYEN_MERCHANT_ACCOUNT,
#                 customer_code=ui_component.customer_code,
#                 token=tokenised_card.token,
#                 ip=ui_component.client_ip,
#                 order_id=ui_component.order_id or response.message['pspReference'],
#                 gateway_response_message=response.message.get('resultCode', '')
#             )
#             tokenised_card.payment = payment
#             tokenised_card.save()
#             return payment
#         raise Exception(response.message.get('refusalReason', 'Pre-auth failed'))

#     def increase_initial_auth(self, tokenised_card):
#         ui_component = tokenised_card.ui_component_request
#         payment = Payment.objects.get(order_id=ui_component.order_id)
#         amount_update_request = {
#             'merchantAccount': settings.ADYEN_MERCHANT_ACCOUNT,
#             'amount': {'value': int(ui_component.amount_to_charge * 100), 'currency': 'AUD'},
#             'reference': ui_component.idempotency_key or f"increase_{uuid.uuid4()}",
#             'originalReference': payment.bank_transaction_id
#         }
#         response = self.adyen.checkout.amount_updates(payment.bank_transaction_id, amount_update_request)

#         if response.message.get('status') == 'received':
#             payment.amount = ui_component.amount_to_charge
#             payment.save()
#             new_payment = Payment.objects.create(
#                 bank_transaction_id=response.message['pspReference'],
#                 amount=ui_component.amount_to_charge,
#                 currency='AUD',
#                 status='Authorised',
#                 is_init_aut=True,
#                 merchant_code=ui_component.merchant_code or settings.ADYEN_MERCHANT_ACCOUNT,
#                 customer_code=ui_component.customer_code,
#                 token=tokenised_card.token,
#                 gateway_response_message='Authorised'
#             )
#             tokenised_card.payment = new_payment
#             tokenised_card.save()
#             return new_payment
#         raise Exception('Amount update failed')

#     def cancel_initial_auth(self, tokenised_card):
#         ui_component = tokenised_card.ui_component_request
#         payment = Payment.objects.get(order_id=ui_component.order_id)
#         cancel_request = {
#             'merchantAccount': settings.ADYEN_MERCHANT_ACCOUNT,
#             'originalReference': payment.bank_transaction_id,
#             'reference': ui_component.idempotency_key or f"cancel_{uuid.uuid4()}"
#         }
#         response = self.adyen.checkout.cancels(cancel_request)

#         if response.message.get('status') == 'received':
#             payment.status = 'Cancelled'
#             payment.save()
#             new_payment = Payment.objects.create(
#                 bank_transaction_id=response.message['pspReference'],
#                 amount=payment.amount,
#                 currency='AUD',
#                 status='Cancelled',
#                 is_init_aut=True,
#                 merchant_code=ui_component.merchant_code or settings.ADYEN_MERCHANT_ACCOUNT,
#                 customer_code=ui_component.customer_code,
#                 token=tokenised_card.token,
#                 gateway_response_message='Cancelled'
#             )
#             tokenised_card.payment = new_payment
#             tokenised_card.save()
#             return new_payment
#         raise Exception('Cancel failed')

#     def capture_initial_auth(self, tokenised_card):
#         ui_component = tokenised_card.ui_component_request
#         payment = Payment.objects.get(order_id=ui_component.order_id)
#         capture_request = {
#             'merchantAccount': settings.ADYEN_MERCHANT_ACCOUNT,
#             'amount': {'value': int(ui_component.amount_to_charge * 100), 'currency': 'AUD'},
#             'reference': ui_component.idempotency_key or f"capture_{uuid.uuid4()}",
#             'originalReference': payment.bank_transaction_id
#         }
#         response = self.adyen.checkout.captures(capture_request)

#         if response.message.get('status') == 'received':
#             payment.status = 'Captured'
#             payment.amount = ui_component.amount_to_charge
#             payment.save()
#             new_payment = Payment.objects.create(
#                 bank_transaction_id=response.message['pspReference'],
#                 amount=ui_component.amount_to_charge,
#                 currency='AUD',
#                 status='Captured',
#                 merchant_code=ui_component.merchant_code or settings.ADYEN_MERCHANT_ACCOUNT,
#                 customer_code=ui_component.customer_code,
#                 token=tokenised_card.token,
#                 gateway_response_message='Captured'
#             )
#             tokenised_card.payment = new_payment
#             tokenised_card.save()
#             return new_payment
#         raise Exception('Capture failed')

#     def get_payment_instruments(self, customer_code):
#         return PaymentInstrument.objects.filter(customer_code=customer_code, deleted=False)

#     def delete_payment_instrument(self, customer_code, token):
#         self.adyen.recurring.disable_stored_payment_method({
#             'merchantAccount': settings.ADYEN_MERCHANT_ACCOUNT,
#             'shopperReference': customer_code,
#             'recurringDetailReference': token
#         })
#         payment_instrument = PaymentInstrument.objects.get(customer_code=customer_code, token=token)
#         payment_instrument.delete()
#         return True

#     def retrieve_public_key(self, client_id):
#         return {
#             'publicKey': settings.ADYEN_CLIENT_KEY,
#             'uiComponentSource': (settings.ADYEN_UI_COMPONENT_SOURCE_TEST
#                                  if settings.ADYEN_ENVIRONMENT == 'Test'
#                                  else settings.ADYEN_UI_COMPONENT_SOURCE_LIVE)
#         }

#     def retrieve_token(self, card_token_request):
#         card_holder = card_token_request.card_holder_detail
#         card_data = {
#             'number': card_token_request.instrument,
#             'expiryMonth': str(card_token_request.expiry_month),
#             'expiryYear': str(card_token_request.expiry_year),
#             'cvc': card_token_request.cvv,
#             'holderName': f"{card_holder.first_name} {card_holder.last_name}".strip()
#         }
#         payment_request = {
#             'merchantAccount': settings.ADYEN_MERCHANT_ACCOUNT,
#             'amount': {'value': 0, 'currency': 'AUD'},
#             'reference': f"token_{uuid.uuid4()}",
#             'paymentMethod': card_data,
#             'storePaymentMethod': card_token_request.save_for_future,
#             'shopperReference': card_token_request.customer_code,
#             'shopperInteraction': 'Ecommerce',
#             'recurringProcessingModel': 'CardOnFile',
#             'returnUrl': 'https://your-company.com/redirect'
#         }
#         response = self.adyen.checkout.payments(payment_request)

#         if response.message.get('resultCode') == 'Authorised':
#             payment = Payment.objects.create(
#                 bank_transaction_id=response.message['pspReference'],
#                 amount=0,
#                 currency='AUD',
#                 status=response.message.get('resultCode', ''),
#                 gateway_response_message=response.message.get('resultCode', ''),
#                 customer_code=card_token_request.customer_code
#             )
#             tokenised_card = TokenisedCard.objects.create(
#                 card_token_request=card_token_request,
#                 card_holder_detail=card_token_request.card_holder_detail,
#                 payment=payment,
#                 token=response.message['additionalData']['recurring.recurringDetailReference'],
#                 save_card_for_future=card_token_request.save_for_future,
#                 brand_type=response.message.get('paymentMethod', {}).get('brand', ''),
#                 customer_code=card_token_request.customer_code,
#                 merchant_reference=response.message['merchantReference'],
#                 scheme=response.message.get('paymentMethod', {}).get('type', ''),
#                 bin=card_data['number'][:6],
#                 last4=card_data['number'][-4:],
#                 expiry_month=str(card_token_request.expiry_month).zfill(2),
#                 expiry_year=str(card_token_request.expiry_year)
#             )
#             return tokenised_card
#         raise Exception(response.message.get('refusalReason', 'Tokenization failed'))

#     def account_verification(self, tokenised_card):
#         ui_component = tokenised_card.ui_component_request
#         payment_request = {
#             'merchantAccount': settings.ADYEN_MERCHANT_ACCOUNT,
#             'amount': {'value': 0, 'currency': 'AUD'},
#             'reference': ui_component.idempotency_key or f"verify_{uuid.uuid4()}",
#             'paymentMethod': {
#                 'type': 'scheme',
#                 'storedPaymentMethodId': tokenised_card.token
#             },
#             'shopperReference': ui_component.customer_code,
#             'shopperInteraction': 'Ecommerce',
#             'recurringProcessingModel': 'CardOnFile',
#             'returnUrl': 'https://your-company.com/redirect',
#             'shopperIP': ui_component.client_ip
#         }
#         response = self.adyen.checkout.payments(payment_request)

#         if response.message.get('resultCode') == 'Authorised':
#             payment = Payment.objects.create(
#                 bank_transaction_id=response.message['pspReference'],
#                 amount=0,
#                 currency='AUD',
#                 status=response.message['resultCode'],
#                 customer_code=ui_component.customer_code,
#                 ip=ui_component.client_ip,
#                 gateway_response_message='Verified'
#             )
#             tokenised_card.payment = payment
#             tokenised_card.save()
#             return payment
#         raise Exception(response.message.get('refusalReason', 'Verification failed'))