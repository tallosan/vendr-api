#
# Contract template serializer.
#
# @author :: tallosan
# ================================================================

from transaction.serializers import ContractSerializer
from transaction.models import AbstractContractFactory


class TemplateContractSerializer(ContractSerializer):
    """
    Template contract serializer. We just need to override the creation
    method, as that's the only area where the two serializers differ.
    """

    class Meta(ContractSerializer.Meta):
        fields = ContractSerializer.Meta.fields + ("is_template", )

    def create(self, validated_data):
        """
        Create a contract with the necesasry template-specific settings.
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

