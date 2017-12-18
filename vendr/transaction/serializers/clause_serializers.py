#
# Serializers for Clause models.
#
# @author :: tallosan
# =====================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from transaction.models import Clause, StaticClause, DynamicClause


class ClauseSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
                "id",
                "title",
                "is_active",
                "preview",
                "explanation"
        )
      
    def to_representation(self, instance):

        clause = super(ClauseSerializer, self).to_representation(instance)
        contract = instance.contract
        if (not contract.is_template) and (contract.transaction.stage == 2):
            clause["doc_ref"] = instance._doc_ref

        return clause


class GenericClauseSerializer(ClauseSerializer):
    """
    Generic serializer for any valid clause type.
    """

    def to_representation(self, instance):
        """
        Serializer the clause with the appropriate serializer type.
        Args:
            `instance` (Clause) -- The clause being serializer.
        """

        if isinstance(instance, StaticClause):
            serializer = StaticClauseSerializer()
        elif isinstance(instance, DynamicClause):
            serializer = DynamicClauseSerializer()
            instance = instance.actual_type
        else:
            raise ValueError("error: invalid clause type given.")

        return serializer.to_representation(instance)


class StaticClauseSerializer(ClauseSerializer):
    """
    Serializer for static clauses.
    """

    class Meta(ClauseSerializer.Meta):
        model = StaticClause


class DynamicClauseSerializer(ClauseSerializer):
    """
    Serializer for dynamic clauses.
    """

    class Meta(ClauseSerializer.Meta):
        model  = DynamicClause
        fields = ClauseSerializer.Meta.fields + (
                "generator",
                "comment",
                "rejected"
        )
        validators = []
    
    #TODO: This should be done better.
    def to_internal_value(self, data):
        return data
    
    def to_representation(self, instance):
        
        clause = super(DynamicClauseSerializer, self).to_representation(instance)
        clause['generator'] = instance.generator
        
        return clause


class DropdownClauseSerializer(DynamicClauseSerializer):
    """
    Serializer for dynamic dropdown clauses.
    """

    class Meta(DynamicClauseSerializer.Meta):
        model  = DynamicClause
        
