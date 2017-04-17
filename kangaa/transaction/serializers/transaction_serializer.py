#
# Serializers for Transactions.
#
# =====================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from transaction.models import Transaction, Offer, Contract
from .nested_serializers import OfferSerializer, ContractSerializer

User = get_user_model()


'''   Serializer for Transactions. '''
class TransactionSerializer(serializers.ModelSerializer):
    
    buyer       = serializers.ReadOnlyField(source='buyer.id')
    
    #TODO: Separate Buyer and Seller offers.
    #TODO: Separate Buyer and Seller contracts.
    offers      = OfferSerializer(Offer.objects.all(), many=True)
    contracts   = ContractSerializer(Contract.objects.all(), many=True, required=False)

    class Meta:
        model  = Transaction
        fields = (
                    'id',
                    'buyer', 'seller',
                    'kproperty',
                    'stage',
                    'offers',
                    'contracts',
                    'start_date',
        )

    def create(self, validated_data):
        
        # Get the buyer, seller, and 
        buyer     = validated_data.pop('buyer')
        seller    = validated_data.pop('seller')
        kproperty = validated_data.pop('kproperty')
        
        offer_data = validated_data.pop('offers')[0]
        
        trans = Transaction.objects.create_transaction(buyer=buyer, seller=seller,
                    kproperty=kproperty,
                    **validated_data
        )
        
        # Create the offer.
        Offer.objects.create(owner=buyer, transaction=trans, **offer_data)
        
        print 'created', trans
        print 'created offer', trans.offers
        print 'done creation'
        return trans

    def update(self, instance, validated_data):
        
        print 'UPDATE: '
        print instance
        print validated_data

