#
# Serializers for Transactions.
#
# =====================================================================

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import serializers

from transaction.models import Transaction, Offer, Contract
from transaction.exceptions import BadTransactionRequest

from .offer_serializer import OfferSerializer
from .contract_serializer import ContractSerializer

User = get_user_model()


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transactions.
    """
    
    buyer = serializers.ReadOnlyField(source="buyer.id")
    
    offers = OfferSerializer(Offer.objects.all(), many=True, required=True)
    contracts = ContractSerializer(Contract.objects.all(), many=True, required=False)
    closing = serializers.PrimaryKeyRelatedField(read_only=True)
    
    deposit = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = (
                "id",
                "start_date",
                "buyer",
                "seller",
                "kproperty",
                "stage",
                "offers",
                "buyer_accepted_offer",
                "seller_accepted_offer",
                "contracts_equal",
                "buyer_accepted_contract",
                "seller_accepted_contract",
                "contracts",
                "closing",
                "payment",
                "deposit"
        )

    def create(self, validated_data):
        """
        Create a new Transaction. Each transaction begins/is created with a
        single initial offer. Note, whilst the Offer is created here, we
        defer Transaction creation to the Transaction Custom Manager.
        Args:
            `validated_data` (dict) -- The data for the transaction.
        """
        
        # Get the buyer, seller, and property.
        buyer     = validated_data.pop("buyer")
        seller    = validated_data.pop("seller")
        kproperty = validated_data.pop("kproperty")
        
        offer_data = validated_data.pop("offers")[0]
        try:
            trans = Transaction.objects.create_transaction(buyer=buyer, seller=seller,
                        kproperty=kproperty,
                        **validated_data
            )
        except IntegrityError:
            error_msg = {
                    "error": "a transaction on property " + str(kproperty.pk) + \
                    " by user " + str(buyer.pk) + " already exists."
            }
            raise BadTransactionRequest(error_msg)

        # Create the offer.
        Offer.objects.create(owner=buyer, transaction=trans, **offer_data)

        return trans

    def update(self, instance, validated_data):
        """
        Update a Transaction. We enforce field level permissions here.
        Args:
            instance (Transaction) -- The Transaction model to update.
            validated_data (dict) -- The Transaction update data.
        """
        print validated_data
        
        # Go through each given field, and perform an update.
        for field in validated_data.keys():
            target_data = validated_data.pop(field)
            target = getattr(instance, field)

            if field == "stage":
                try: instance.advance_stage()
                except ValueError as msg:
                    raise BadTransactionRequest({"error": str(msg)})
            else:
                setattr(instance, field, target_data)

            instance.save()

        return instance

    def to_representation(self, instance):
        """
        Transaction representation. Returns the offer data split into two separate
        entities; buyer offers, and seller offers, along with the contract data
        in the same manner.
        Args:
            instance (Transaction) -- The Transaction model being serialized.
        """
            
        transaction = super(TransactionSerializer, self).to_representation(instance)
        transaction["offers"] = self.format_offers(instance)
              
        return transaction

    def format_offers(self, instance):
        """
        (Helper) Format the Offers made by the buyer and seller involved in a
        given transaction.
        Args:
            instance (Transaction) -- The Transaction model being serialized.
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

    def get_deposit(self, instance):
        """
        Retrieves the deposit amount (if any) for the given transaction.
        Args:
            `instance` (Transaction) -- The transaction we're serializing.
        """
        
        deposit = None
        
        accepted_offer = getattr(instance, "seller_accepted_offer", None)
        if accepted_offer:
            deposit = Offer.objects.get(pk=accepted_offer).deposit

        return deposit

