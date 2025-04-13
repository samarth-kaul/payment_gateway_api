from django.db import models

class UIComponentRequest(models.Model):
    merchant_code = models.CharField(max_length=100, blank=True)
    client_id = models.CharField(max_length=100, blank=True)
    customer_code = models.CharField(max_length=100)
    order_id = models.CharField(max_length=255, blank=True)
    idempotency_key = models.CharField(max_length=255, blank=True)
    amount_to_charge = models.DecimalField(max_digits=10, decimal_places=2)
    client_ip = models.GenericIPAddressField(blank=True, null=True)
    required_card_holder_detail = models.BooleanField(default=False)
    transaction_type = models.CharField(max_length=50, blank=True)
    ui_component_string = models.CharField(max_length=255, blank=True)


