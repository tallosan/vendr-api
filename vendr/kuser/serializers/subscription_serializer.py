#
# Serializer for a User object's transactions.
#
# ========================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from transaction.models import Transaction

User = get_user_model()


class SubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('subscriptions', )

