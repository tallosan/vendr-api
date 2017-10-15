#
# Serializer for a User object's transactions.
#
# ========================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException

User = get_user_model()


class TwoFactorAuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('tfa_enabled', 'tfa_code', '_tfa_code_validated')

    def update(self, instance, validated_data):

        protected_field = validated_data.pop('_tfa_code_validated', None)
        if protected_field:
            raise ValueError(
                    '`_tfa_code_validated` is a protected field, and '
                    'cannot be changed.'
            )

        tfa_code = validated_data.pop('tfa_code', None)
        if tfa_code:
            if instance.tfa_code == tfa_code:
                instance.tfa_code = tfa_code
                instance._tfa_code_validated = True
                instance.save()
            else:
                raise ValueError('the given `tfa_code` does not match.')

        tfa_enabled = validated_data.pop('tfa_enabled', None)
        if tfa_enabled is not None:
            if tfa_enabled is True: instance._tfa_code_validated = False
            instance.tfa_enabled = tfa_enabled
            instance.save()

        return instance

    """ We want users to be able to modify their `tfa_code`, however we
        don't want to actually show it in the serialized response, as
        that of course would be a security vulnerability.
        Args:
            instance (KUser) -- The user model who owns this endpoint.
    """
    def to_representation(self, instance):

        tfa = super(TwoFactorAuthSerializer, self).to_representation(instance)
        tfa.pop('tfa_code')

        return tfa

