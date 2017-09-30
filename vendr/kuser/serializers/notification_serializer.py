#
# Serializers for Notifications.
#
# =====================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from kuser.models import TransactionNotification, OfferNotification, \
                            ContractNotification, \
                            TransactionWithdrawNotification, \
                            AdvanceStageNotification, \
                            OpenHouseStartNotification


class NotificationSerializer(serializers.ModelSerializer):

    recipient = serializers.PrimaryKeyRelatedField(source='recipient.pk', read_only=True)

    class Meta:
        fields = ('id',
                  'recipient',
                  'description',
                  'is_viewed',
                  'timestamp'
        )


class TransactionWithdrawNotificationSerializer(NotificationSerializer):

    class Meta(NotificationSerializer.Meta):
        model = TransactionWithdrawNotification


class AdvanceStageNotificationSerializer(NotificationSerializer):
    class Meta(NotificationSerializer.Meta):
        model = AdvanceStageNotification


class OpenHouseStartNotificaitonSerializer(NotificationSerializer):

    class Meta(NotificationSerializer.Meta):
        model = OpenHouseStartNotification


class TransactionNotificationSerializer(NotificationSerializer):

    class Meta(NotificationSerializer.Meta):
        model  = TransactionNotification
        fields = NotificationSerializer.Meta.fields + ('transaction', '_type')


class OfferNotificationSerializer(TransactionNotificationSerializer):

    class Meta(TransactionNotificationSerializer.Meta):
        model  = OfferNotification
        fields = TransactionNotificationSerializer.Meta.fields + ('offer', )


class ContractNotificationSerializer(TransactionNotificationSerializer):

    class Meta(TransactionNotificationSerializer.Meta):
        model  = ContractNotification
        fields = TransactionNotificationSerializer.Meta.fields + ('contract', )

