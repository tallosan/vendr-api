#
# Serializers for Notifications.
#
# =====================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from kuser.models import BaseNotification, \
        TransactionNotification, OfferNotification, \
        ContractNotification, \
        TransactionWithdrawNotification, \
        AdvanceStageNotification, \
        ClauseChangeNotification


class BaseNotificationSerializer(serializers.ModelSerializer):

    recipient = serializers.PrimaryKeyRelatedField(
            source='recipient.pk',
            read_only=True
    )
    _type = serializers.SerializerMethodField()

    class Meta:
        model = BaseNotification
        fields = ('id',
                  'recipient',
                  'description',
                  'resource',
                  'is_viewed',
                  'timestamp',
                  '_type'
        )

    def get__type(self, instance):
        return instance._type


class TransactionNotificationSerializer(BaseNotificationSerializer):

    class Meta(BaseNotificationSerializer.Meta):
        model  = TransactionNotification
        fields = BaseNotificationSerializer.Meta.fields + ('transaction', )


class OfferNotificationSerializer(TransactionNotificationSerializer):

    class Meta(TransactionNotificationSerializer.Meta):
        model  = OfferNotification
        fields = TransactionNotificationSerializer.Meta.fields + ('offer', )


class ContractNotificationSerializer(TransactionNotificationSerializer):

    class Meta(TransactionNotificationSerializer.Meta):
        model  = ContractNotification
        fields = TransactionNotificationSerializer.Meta.fields + ('contract', )

