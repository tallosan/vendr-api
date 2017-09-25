#
# Serializer for a User's contracts.
#
# ========================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from transaction.models import Transaction, Contract

User = get_user_model()


"""   Stripped down serializer for a user's contracts. """
class UserContractSerializer(serializers.ModelSerializer):

    incoming = serializers.SerializerMethodField()
    outgoing = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('incoming', 'outgoing')

    """ Returns a list of incoming contract PKs. """
    def get_incoming(self, instance):

        incoming_contracts = []
        for transaction in Transaction.objects.filter(seller=instance.pk):
            try:
                contract_pk = transaction.contracts.\
                    values_list('pk', flat=True).get(owner=instance)
                incoming_contracts.append(contract_pk)
            except Contract.DoesNotExist:
                pass

        return incoming_contracts

    """ Returns a list of outgoing contract PKs. """
    def get_outgoing(self, instance):

        outgoing_contracts = []
        for transaction in Transaction.objects.filter(buyer=instance.pk):
            try:
                contract_pk = transaction.contracts.\
                    values_list('pk', flat=True).get(owner=instance)
                outgoing_contracts.append(contract_pk)
            except Contract.DoesNotExist:
                pass
       
        return outgoing_contracts

