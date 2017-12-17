#
# Contract template serializer.
#
# @author :: tallosan
# ================================================================

from rest_framework import serializers

from django.conf import settings

from transaction.serializers import ContractSerializer, StaticClauseSerializer, \
        DynamicClauseSerializer, GenericClauseSerializer
from transaction.models import AbstractContractFactory, Contract, \
        StaticClause, DynamicClause


class TemplateContractSerializer(ContractSerializer):
    """
    Template contract serializer. We just need to override the creation
    method, as that's the only area where the two serializers differ.
    """

    def create(self, validated_data):
        """
        Create a contract with the necesasry template-specific settings.
        Args:
            `validated_data` (dict) -- The data we're using to create our template.
        """

        ctype = validated_data.pop("ctype", None)
        owner = validated_data.pop("owner", None)
        assert ctype and owner, (
                "error: contract type and owner must both be specified."
        )

        template = AbstractContractFactory.create_contract(
                ctype,
                owner=owner,
                transaction=None,
                **validated_data
        )

        return template

    def get_clauses(self, instance):
        """
        Custom URL representation.
        Args:
            `instance` (Contract) -- The Contract being serialized.
        """

        clauses = '{}users/{}/templates/{}/clauses/'.format(
            settings.BASE_URL, instance.owner.pk, instance.pk
        )
        
        return clauses

