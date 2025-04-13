from django.db import models
from .fraud_check_result import FraudCheckResult

class Payment(models.Model):
    is_init_auth = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    merchant_code = models.CharField(max_length=100, blank=True)
    customer_code = models.CharField(max_length=100, blank=True)
    token = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    order_id = models.CharField(max_length=50)
    bank_transaction_id = models.CharField(max_length=255, blank=True)
    gateway_response_code = models.CharField(max_length=50, blank=True, null=True)
    gateway_response_message = models.CharField(max_length=255, blank=True)
    error_code = models.CharField(max_length=20, blank=True, null=True)
    fraud_check_type = models.CharField(max_length=20, blank=True, null=True)
    fraud_check_result = models.OneToOneField(FraudCheckResult, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Payment - Order {self.order_id}"

    class Meta:
        db_table = 'payment'