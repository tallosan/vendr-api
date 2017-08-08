#
# Serializers for Notifications.
#
# =====================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from kuser.models import TransactionNotification, OfferNotification, \
                            ContractNotification


class NotificationSerializer(serializers.ModelSerializer):

    recipient = serializers.PrimaryKeyRelatedField(source='recipient.pk', read_only=True)

    class Meta:
        fields = ('id',
                  'recipient',
                  'description',
                  'is_viewed',
                  'timestamp'
        )

        
class TransactionNotificationSerializer(NotificationSerializer):

    class Meta(NotificationSerializer.Meta):
        model  = TransactionNotification
        fields = NotificationSerializer.Meta.fields + ('transaction', )


class OfferNotificationSerializer(TransactionNotificationSerializer):

    class Meta(TransactionNotificationSerializer.Meta):
        model  = OfferNotification
        fields = TransactionNotificationSerializer.Meta.fields + ('offer', )


class ContractNotificationSerializer(TransactionNotificationSerializer):

    class Meta(TransactionNotificationSerializer.Meta):
        model  = ContractNotification
        fields = TransactionNotificationSerializer.Meta.fields + ('contract', )
