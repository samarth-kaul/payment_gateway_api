from django.db import models

class FraudCheckResult(models.Model):
    provider_reference_number = models.CharField(max_length=255, blank=True)
    score = models.IntegerField(default=0)
    provider_response_message = models.TextField()

    def __str__(self):
        return f"Score: {self.score} - Ref: {self.provider_reference_number}"

    class Meta:
        db_table = 'fraud_check_result'
