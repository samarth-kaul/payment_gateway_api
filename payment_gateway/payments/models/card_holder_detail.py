from django.db import models

class CardHolderDetail(models.Model):
    frequent_flyer_number = models.CharField(max_length=100)
    ref_title = models.BigIntegerField(default=0)
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    is_required_tax_invoice = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # class Meta:
    #     db_table = 'card_holder_detail'