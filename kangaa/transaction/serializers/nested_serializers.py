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
    
    owner = serializers.ReadOnlyField(source='owner.email')
    
    class Meta:
        model   = Offer
        fields = (
                    'id',
                    'owner',
                    'offer',
                    'deposit',
                    'comment',
                    'is_accepted',
                    'timestamp',
        )


'''   Serializer for Contracts. '''
class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Contract
        fields = ()

