#
# Serializer for a User object's transactions.
#
# ========================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from transaction.models import Transaction

User = get_user_model()


class UserTransactionSerializer(serializers.ModelSerializer):

    incoming = serializers.SerializerMethodField()
    outgoing = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('incoming', 'outgoing')

    def get_incoming(self, instance):
        return Transaction.objects.filter(seller=instance.pk).\
                values_list('pk', flat=True)

    def get_outgoing(self, instance):
        return Transaction.objects.filter(buyer=instance.pk).\
                values_list('pk', flat=True)

