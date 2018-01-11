#
# Payment serializers.
#
# @author :: tallosan
# ================================================================

from rest_framework import serializers

from django.contrib.auth import get_user_model

from kuser.serializers import GenericAccountSerializer
from payment.models import Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for payment creation and retrieval.
    """

    payee = serializers.PrimaryKeyRelatedField(
            required=False,
            queryset=User.objects.all()
    )
    recipient = serializers.PrimaryKeyRelatedField(
            required=False,
            queryset=User.objects.all()
    )

    class Meta:
        model = Payment
        fields = (
                "pk",
                "payee",
                "recipient",
                "payee_account",
                "recipient_account",
                "amount",
                "message",
                "timestamp",
        )

    def update(self, instance, validated_data):
        """
        Get the given Account models (if any), and set them.
        """

        # Payee account.
        payee_account = validated_data.pop("payee_account", None)
        if payee_account:
            instance.payee_account = payee_account

        # Recipient account.
        recipient_account = validated_data.pop("recipient_account", None)
        if recipient_account:
            instance.recipient_account = recipient_account

        instance.save()
        return super(PaymentSerializer, self).update(
                instance,
                validated_data
        )

