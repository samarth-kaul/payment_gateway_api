# from django.db import models

# class CardHolderDetail(models.Model):
#     frequent_flyer_number = models.CharField(max_length=100, blank=True)
#     ref_title = models.BigIntegerField(null=True, blank=True)
#     title = models.CharField(max_length=50, blank=True)
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(blank=True)
#     is_required_tax_invoice = models.BooleanField(default=False)
#     is_default = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

# class CardTokenRequest(models.Model):
#     card_holder_detail = models.ForeignKey(CardHolderDetail, on_delete=models.CASCADE, null=True)
#     instrument = models.CharField(max_length=19)
#     cvv = models.CharField(max_length=4)
#     expiry_month = models.IntegerField()
#     expiry_year = models.IntegerField()
#     scheme = models.CharField(max_length=50, blank=True)
#     save_for_future = models.BooleanField(default=True)
#     customer_code = models.CharField(max_length=100)

#     def __str__(self):
#         return f"Card ending {self.instrument[-4:]}"

# class FraudCheckResult(models.Model):
#     provider_reference_number = models.CharField(max_length=255, blank=True)
#     score = models.IntegerField(default=0)
#     provider_response_message = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return f"FraudCheck {self.provider_reference_number}"

# class Payment(models.Model):
#     is_init_auth = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     merchant_code = models.CharField(max_length=100, blank=True)
#     customer_code = models.CharField(max_length=100, blank=True)
#     token = models.CharField(max_length=255, blank=True)
#     ip = models.GenericIPAddressField(blank=True, null=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=50)
#     order_id = models.CharField(max_length=255, blank=True)
#     bank_transaction_id = models.CharField(max_length=255, blank=True)
#     gateway_response_code = models.CharField(max_length=50, blank=True)
#     gateway_response_message = models.CharField(max_length=255, blank=True)
#     error_code = models.CharField(max_length=50, blank=True)
#     fraud_check_type = models.CharField(max_length=50, blank=True)
#     fraud_check_result = models.ForeignKey(FraudCheckResult, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return self.bank_transaction_id or str(self.id)

# class PaymentInstrument(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     customer_code = models.CharField(max_length=100)
#     brand_type = models.CharField(max_length=50, blank=True)
#     brand_category = models.CharField(max_length=50, blank=True)
#     token = models.CharField(max_length=255, unique=True)
#     scheme = models.CharField(max_length=50, blank=True)
#     last4 = models.CharField(max_length=4, blank=True)
#     expiry_month = models.CharField(max_length=2, blank=True)
#     expiry_year = models.CharField(max_length=4, blank=True)

#     def __str__(self):
#         return f"{self.scheme} ending {self.last4}"

# class UIComponentRequest(models.Model):
#     merchant_code = models.CharField(max_length=100, blank=True)
#     client_id = models.CharField(max_length=100, blank=True)
#     customer_code = models.CharField(max_length=100)
#     order_id = models.CharField(max_length=255, blank=True)
#     idempotency_key = models.CharField(max_length=255, blank=True)
#     amount_to_charge = models.DecimalField(max_digits=10, decimal_places=2)
#     client_ip = models.GenericIPAddressField(blank=True, null=True)
#     required_card_holder_detail = models.BooleanField(default=False)
#     transaction_type = models.CharField(max_length=50, blank=True)
#     ui_component_string = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return f"Request for {self.customer_code} - {self.amount_to_charge}"

# class TokenisedCard(models.Model):
#     ui_component_request = models.ForeignKey(UIComponentRequest, on_delete=models.CASCADE, null=True)
#     card_holder_detail = models.ForeignKey(CardHolderDetail, on_delete=models.CASCADE, null=True)
#     payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
#     card_token_request = models.ForeignKey(CardTokenRequest, on_delete=models.CASCADE, null=True)
#     merchant_code = models.CharField(max_length=100, blank=True)
#     token = models.CharField(max_length=255, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     scheme = models.CharField(max_length=50, blank=True)
#     bin = models.CharField(max_length=6, blank=True)
#     last4 = models.CharField(max_length=4, blank=True)
#     expiry_month = models.CharField(max_length=2, blank=True)
#     expiry_year = models.CharField(max_length=4, blank=True)
#     customer_code = models.CharField(max_length=100, blank=True)
#     brand_type = models.CharField(max_length=50, blank=True)
#     brand_category = models.CharField(max_length=50, blank=True)
#     merchant_reference = models.CharField(max_length=255, blank=True)
#     save_card_for_future = models.BooleanField(default=True)
#     deleted = models.BooleanField(default=False)
#     is_new = models.BooleanField(default=True)

#     def __str__(self):
#         return f"TokenisedCard {self.token}"

#     @property
#     def pan(self):
#         bin_part = self.bin or ""
#         last4_part = self.last4 or ""
#         return bin_part.ljust(12, "X") + last4_part.rjust(4, "X")

#     @property
#     def expiry_date(self):
#         return f"{self.expiry_month}/{self.expiry_year}"

#     @property
#     def card_type(self):
#         return self.scheme