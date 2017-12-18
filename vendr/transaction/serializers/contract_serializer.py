#
# Serializers for Contract models.
#
# @author :: tallosan
# =====================================================================

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers

from transaction.models import Contract, AbstractContractFactory
from transaction.exceptions import BadTransactionRequest

User = get_user_model()


class ContractSerializer(serializers.ModelSerializer):
    """
    Serializer for Contracts.
    """

    owner = serializers.ReadOnlyField(source="owner.pk")
    clauses = serializers.SerializerMethodField()

    class Meta:
        model  = Contract
        fields = (
                "id",
                "owner",
                "clauses",
                "timestamp",
        )

    def get_clauses(self, instance):
        """
        Custom URL representation.
        Args:
            `instance` (Contract) -- The Contract being serialized.
        """

        clauses = None
        if not instance.is_template:
            clauses = '{}transactions/{}/contracts/{}/clauses/'.format(
                settings.BASE_URL,
                instance.transaction.pk,
                instance.pk
            )
        
        return clauses

    def create(self, validated_data):
        """
        Create a contract of the given type.
        Args:
            `validated_data` (OrderedDict) -- The request data we create the contract from.
        """
        
        ctype = validated_data.pop("ctype")
        owner = validated_data.pop("owner")
        transaction = validated_data.pop("transaction")
        
        try:
            contract = AbstractContractFactory.create_contract(
                    ctype,
                    owner=owner,
                    transaction=transaction
            )
        except ValueError:
            error_msg = {
                    "error": "{} already has a contract for this transaction".\
                            format(owner.email)
            }
            raise BadTransactionRequest(error_msg)
        
        return contract

