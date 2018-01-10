#
# Account serializers.
#
# @author :: tallosan
# ================================================================

from rest_framework import serializers

from kuser.models import BaseAccount, BankAccount


class BaseAccountSerializer(serializers.ModelSerializer):
    """
    Base account serializer.
    """

    class Meta:
        model = BaseAccount
        fields = (
                "pk",
                "owner"
        )


class BankAccountSerializer(BaseAccountSerializer):
    """
    Bank account serializer.
    """

    class Meta(BaseAccountSerializer.Meta):
        model = BankAccount
        fields = BaseAccountSerializer.Meta.fields + (
                "bank",
                "insitution_number",
                "branch_number",
                "account_number",
        )


class GenericAccountSerializer(serializers.ModelSerializer):
    """
    Generic account serializer that can be used to serializer any
    account type.
    """

    def to_representation(self, instance):
        """
        Downcast the given instance, and serializer it using the
        appropriate serializer. 
        """

        # TODO: Allow generic reads.

        # Downcast.
        if hasattr(instance, "bankaccount"):
            serializer = BankAccountSerializer()
            instance = instance.bankaccount

        to_representation = serializer.to_representation(instance)
        return to_representation

