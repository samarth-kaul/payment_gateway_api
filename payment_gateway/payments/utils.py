import Adyen
from django.conf import settings

def get_adyen_client():
    adyen = Adyen.Adyen()
    adyen.payment.client.api_key = settings.ADYEN_API_KEY
    adyen.payment.client.platform = "test"  # Change to "live" for production
    adyen.payment.client.merchant_account = settings.ADYEN_MERCHANT_ACCOUNT
    return adyen