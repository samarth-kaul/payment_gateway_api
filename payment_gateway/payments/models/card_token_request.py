from django.db import models
from .card_holder_detail import CardHolderDetail

class CardTokenRequest(models.Model):
    card_holder_detail = models.ForeignKey(
        CardHolderDetail,
        on_delete=models.CASCADE,
        null=False,  # Required, but we’ll handle migrations carefully
    )
    instrument = models.CharField(max_length=100)
    cvv = models.CharField(max_length=4)
    expiry_month = models.IntegerField()
    expiry_year = models.IntegerField()
    scheme = models.CharField(max_length=50, blank=True, null=True)
    save_for_future = models.BooleanField(default=False)
    customer_code = models.CharField(max_length=100)

    def __str__(self):
        return f"TokenRequest for {self.customer_code} - {self.instrument[-4:]}"

    # class Meta:
    #     db_table = 'card_token_request'