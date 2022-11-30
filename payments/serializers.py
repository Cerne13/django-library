from .models import Payment
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "payment_type",
            "borrowing_id",
            "session_url",
            "session_id",
            "amount",
        )
        read_only_fields = ("id", "amount")
