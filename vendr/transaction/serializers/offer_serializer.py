#
# Serializers for Offer models.
#
# @author :: tallosan
# =====================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from transaction.models import Offer

User = get_user_model()


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for Offers.
    """
    
    owner = serializers.ReadOnlyField(source="owner.pk")
    
    class Meta:
        model   = Offer
        fields = (
                    "id",
                    "owner",
                    "offer",
                    "deposit",
                    "comment",
                    "timestamp",
        )

    def create(self, validated_data):
        """
        Handles the creation of an Offer object.
        Args:
            `validated_data` (OrderedDict) -- The request data we create the new
                model from.
        """
        
        # Get the owner and transaction pertaining to this Offer.
        owner = validated_data.pop("owner")
        transaction = validated_data.pop("transaction")
        
        offer = Offer.objects.create(
                owner=owner,
                transaction=transaction,
                **validated_data
        )
        
        return offer
    
    def format_offers(self, instance):
        """
        (Helper) Format the Offers made by the buyer and seller involved in a
        given transaction.
        Args:
            `instance` (Offer) -- The Offer model being serialized.
        """
        
        buyer_id = instance.buyer.pk
        seller_id = instance.seller.pk
 
        buyer_offers  = instance.get_offers(user_id=buyer_id)
        seller_offers = instance.get_offers(user_id=seller_id)
 
        offers = {
                    "buyer_offers" : OfferSerializer(buyer_offers, many=True).data,
                    "seller_offers": OfferSerializer(seller_offers, many=True).data
        }
  
        return offers

