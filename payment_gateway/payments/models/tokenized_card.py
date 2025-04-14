from django.db import models
from .card_holder_detail import CardHolderDetail
from .payment import Payment
from .card_token_request import CardTokenRequest
from .ui_component_request import UIComponentRequest

class TokenizedCard(models.Model):
    ui_component_request = models.ForeignKey(
        UIComponentRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    card_holder_detail = models.ForeignKey(
        CardHolderDetail,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    card_token_request = models.ForeignKey(
        CardTokenRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    merchant_code = models.CharField(max_length=100, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    scheme = models.CharField(max_length=50, blank=True, null=True)
    bin = models.CharField(max_length=6, blank=True, null=True)
    last4 = models.CharField(max_length=4, blank=True, null=True)
    expiry_month = models.CharField(max_length=2, blank=True, null=True)
    expiry_year = models.CharField(max_length=4, blank=True, null=True)
    customer_code = models.CharField(max_length=100, blank=True, null=True)
    brand_type = models.CharField(max_length=50, blank=True, null=True)
    brand_category = models.CharField(max_length=50, blank=True, null=True)
    merchant_reference = models.CharField(max_length=255, blank=True, null=True)
    save_card_for_future = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)

    def __str__(self):
        return f"TokenizedCard ending with {self.last4 or 'N/A'}"

    @property
    def pan(self):
        bin_part = self.bin or ""
        last4_part = self.last4 or ""
        return bin_part.ljust(12, "X") + last4_part.rjust(4, "X")

    @property
    def expiry_date(self):
        return f"{self.expiry_month or ''}/{self.expiry_year or ''}"

    @property
    def card_type(self):
        return self.scheme or ''

    # class Meta:
    #     db_table = 'tokenised_card'
