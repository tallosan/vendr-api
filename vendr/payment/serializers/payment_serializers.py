#
# Payment serializers.
#
# @author :: tallosanI
# ================================================================

from rest_framework import serializers

from kuser.models import KUser as User
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for payment creation and retrieval.
    """

    payee = serializers.PrimaryKeyRelatedField(
            required=False,
            queryset=User.objects.all()
    )

    class Meta:
        model = Payment
        fields = (
                "pk",
                "payee",
                "recipient",
                "amount",
                "message",
                "timestamp"
        )

