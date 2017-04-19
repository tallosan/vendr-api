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
    
    # Calls 'get_offers' to separate buyer and seller offers.
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

    ''' Create a new Transaction. Each transaction begins/is created with a
        single initial offer. Note, whilst the Offer is created here, we
        defer Transaction creation to the Transaction Custom Manager.
        Args:
            validated_data: The data for the transaction.
    '''
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
        
        return trans

    ''' Update a Transaction. We enforce field level permissions here.
        Args:
            instance: The Transaction model to update.
            validated_data: The Transaction update data.
    '''
    def update(self, instance, validated_data):

        user = validated_data.pop('user')
        
        # Go through each given field, and perform an update.
        for field in validated_data.keys():
            target_data = validated_data.pop(field)
            target = getattr(instance, field)
            
            # Handle one-to-one keys.
            if type(target_data).__name__ == 'OrderedDict':
                for _field in target_data.keys():
                    setattr(target, _field, target_data[_field])

                target.save()

            # Handle foreign key fields.
            elif type(target_data).__name__ == 'list':
                for model_data in target_data:
                    model_class = target.all().model
                    model_class.objects.create(owner=user, transaction=instance,
                            **model_data)

            # Handle regular attributes.
            else:
                setattr(instance, field, target_data)
        
        return instance

    ''' Transaction representation. Returns the offer data split into two separate
        entities; buyer offers, and seller offers, along with the contract data
        in the same manner.
        Args:
            instance: The Transaction model being serialized.
    '''
    def to_representation(self, instance):
        
        transaction = super(TransactionSerializer, self).to_representation(instance)
        transaction['offers'] = self.format_offers(instance)
              
        return transaction

    ''' (Helper) Format the Offers made by the buyer and seller involved in a
        given transaction.
        Args:
            instance: The Transaction model being serialized.
    '''
    def format_offers(self, instance):
        
        buyer_id = instance.buyer.pk
        seller_id = instance.seller.pk

        buyer_offers  = instance.get_offers(user_id=buyer_id)
        seller_offers = instance.get_offers(user_id=seller_id)

        offers = [
                    { "buyer_offers" : OfferSerializer(buyer_offers, many=True).data },
                    { "seller_offers": OfferSerializer(seller_offers, many=True).data }
        ]
 
        return offers

