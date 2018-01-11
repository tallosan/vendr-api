#
# Payment sub-serializer.
#
# @author :: tallosan
# ================================================================

from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("sent_payments", "received_payments")

