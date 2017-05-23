#
# Serializers for Transaction nested models.
#
# =====================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from transaction.models import Transaction, Offer, Contract, StaticClause,\
    AbstractContractFactory


User = get_user_model()


'''   Serializer for Transactions. '''
class OfferSerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.pk')
    
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
 
        offers = {
                    "buyer_offers" : OfferSerializer(buyer_offers, many=True).data,
                    "seller_offers": OfferSerializer(seller_offers, many=True).data
        }
  
        return offers
      

'''   Serializer for static clauses. '''
class StaticClauseSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaticClause
        fields = ('id',
                  'title',
                  'is_active',
                  'preview',
        )


'''   Serializer for Contracts. '''
class ContractSerializer(serializers.ModelSerializer):

    static_clauses = StaticClauseSerializer(StaticClause.objects.all(), many=True,
                        required=False)

    class Meta:
        model  = Contract
        fields = ('id', 'owner',
                  'static_clauses',#'dynamic_clauses')
                  'timestamp'
        )

    ''' Create a contract of the given type.
        Args:
            validated_data: The request data we create the contract from.
    '''
    def create(self, validated_data):
        
        ctype       = validated_data.pop('ctype')
        owner       = validated_data.pop('owner')
        transaction = validated_data.pop('transaction')
        
        contract = AbstractContractFactory.create_contract(ctype, owner=owner,
                    transaction=transaction)
        
        return contract

