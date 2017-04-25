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
                    'timestamp',
        )

    ''' Handles the creation of an Offer object.
        Args:
            validated_data: The request data we create the new model from.
    '''
    def create(self, validated_data):
        
        # Get the owner and transaction pertaining to this Offer.
        owner       = validated_data.pop('owner')
        transaction = validated_data.pop('transaction')
        
        offer = Offer.objects.create(owner=owner,
                                     transaction=transaction,
                                     **validated_data)
        
        return offer


'''   Serializer for Contracts. '''
class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Contract
        fields = ()

