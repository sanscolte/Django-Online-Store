from rest_framework.serializers import ModelSerializer
from payment.models import BankTransaction


class BankTransactionSerializer(ModelSerializer):
    class Meta:
        model = BankTransaction
        fields = "order", "card_number", "total_price"
