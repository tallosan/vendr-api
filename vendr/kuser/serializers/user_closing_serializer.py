#
# Serializer for a User's closing objects.
#
# ========================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from transaction.models import Transaction, Closing

User = get_user_model()


"""   Stripped down serializer for a user's closing stage objects. """
class UserClosingSerializer(serializers.ModelSerializer):

    incoming = serializers.SerializerMethodField()
    outgoing = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('incoming', 'outgoing')

    """ Returns a list of Closing objects PKs on incoming transactions. """
    def get_incoming(self, instance):

        incoming_contracts = []
        for transaction in Transaction.objects.filter(seller=instance.pk):
            try:
                incoming_contracts.append(transaction.closing.pk)
            except Closing.DoesNotExist:
                pass

        return incoming_contracts

    """ Returns a list of Closing object PKs on outgoing transactions. """
    def get_outgoing(self, instance):

        outgoing_contracts = []
        for transaction in Transaction.objects.filter(buyer=instance.pk):
            try:
                outgoing_contracts.append(transaction.closing.pk)
            except Closing.DoesNotExist:
                pass
       
        return outgoing_contracts

