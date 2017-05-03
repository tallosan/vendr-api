#
# Serializers for Notifications.
#
# =====================================================================

from django.contrib.auth import get_user_model

from rest_framework import serializers

from kuser.models import TransactionNotification, OfferNotification, \
                                ContractNotification


class NotificationSerializer(serializers.ModelSerializer):

    #recipient = serializers.PrimaryKeyRelatedField(source=recipient.pk)

    class Meta:
        fields = ('id',
                  #'recipient',
                  'description',
                  'is_viewed',
                  'timestamp'
        )

        
class TransactionSerializer(NotificationSerializer):

    fields = NotificationSerializer.Meta.fields + ('transaction', )


class OfferSerializer(TransactionSerializer):

    fields = TransactionSerializer.Meta.fields + ('offer', )


class ContractSerializer(TransactionSerializer):

    fields = TransactionSerializer.Meta.fields + ('contract', )


