#
# Serializer for a User object's transactions.
#
# ========================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from kproperty.models import Property

User = get_user_model()


class UserPropertySerializer(serializers.ModelSerializer):

    properties = serializers.PrimaryKeyRelatedField(many=True, required=False,
                    queryset=Property.objects.select_subclasses())

    class Meta:
        model = User
        fields = ('properties', )

