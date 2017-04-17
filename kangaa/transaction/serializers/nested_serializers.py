#
# Serializers for Transaction nested models.
#
# =====================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from transaction.models import Transaction, Offer, Contract


User = get_user_model()


'''   Serializer for Transactions. '''
class OfferSerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.id')
    
    class Meta:
        model   = Offer
        fields = (
                    'owner',
                    'offer',
                    'deposit',
                    'comment',
                    'timestamp',
        )


'''   Serializer for Contracts. '''
class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Contract
        fields = ()

