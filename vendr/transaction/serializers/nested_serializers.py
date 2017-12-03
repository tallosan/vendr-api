#
# Serializers for Transaction nested models.
#
# =====================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from transaction.models import *
from transaction.exceptions import BadTransactionRequest

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


class ClauseSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'is_active', 'preview', 'explanation', "comment")
      
    def to_representation(self, instance):

        clause = super(ClauseSerializer, self).to_representation(instance)
        if instance.contract.transaction.stage == 2:
            clause['doc_ref'] = instance._doc_ref

        return clause


'''   Serializer for static clauses. '''
class StaticClauseSerializer(ClauseSerializer):

    class Meta(ClauseSerializer.Meta):
        model = StaticClause


class DynamicClauseSerializer(ClauseSerializer):

    class Meta(ClauseSerializer.Meta):
        model  = DynamicClause
        fields = ClauseSerializer.Meta.fields + ('generator', )
        validators = []
    
    #TODO: This should be done better.
    def to_internal_value(self, data):
        return data
    
    def to_representation(self, instance):
        
        clause = super(DynamicClauseSerializer, self).to_representation(instance)
        clause['generator'] = instance.generator
        
        return clause


class DropdownClauseSerializer(DynamicClauseSerializer):

    class Meta(DynamicClauseSerializer.Meta):
        model  = DynamicClause


'''   Serializer for Contracts. '''
class ContractSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.pk')
    clauses = serializers.SerializerMethodField()

    class Meta:
        model  = Contract
        fields = ('id', 'owner',
                  'clauses',
                  'timestamp'
        )

    ''' Custom URL representation.
        Args:
            instance: The Contract being serialized.
    '''
    def get_clauses(self, instance):

        return '{}transactions/{}/contracts/{}/clauses/'.format(
                settings.BASE_URL, instance.transaction.pk, instance.pk)

    ''' Create a contract of the given type.
        Args:
            validated_data: The request data we create the contract from.
    '''
    def create(self, validated_data):
        
        ctype       = validated_data.pop('ctype')
        owner       = validated_data.pop('owner')
        transaction = validated_data.pop('transaction')
        
        try:
            contract = AbstractContractFactory.create_contract(ctype,
                        owner=owner, transaction=transaction)
        except ValueError:
            error_msg = { 'error': '{} already has a contract for this transaction'.\
                                   format(owner.email)
            }
            raise BadTransactionRequest(error_msg)
        
        return contract

