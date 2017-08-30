#
# Closing stage serializers.
#
# ===========================================================================


from django.conf import settings

from rest_framework import serializers

from transaction.models import Closing, Document


class ClosingSerializer(serializers.ModelSerializer):
    
    transaction = serializers.ReadOnlyField(source='transaction.pk')
    buyer = serializers.ReadOnlyField(source='transaction.buyer.pk')
    seller = serializers.ReadOnlyField(source='transaction.seller.pk')
    
    class Meta:
        model = Closing
        fields = ('pk', 'transaction', 'buyer', 'seller')


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('pk', 'title', 'content', 'explanation', 'signing_date')


class ClauseDocumentSerializer(DocumentSerializer):

    approved_clauses = serializers.SerializerMethodField()
    pending_clauses = serializers.SerializerMethodField()

    class Meta(DocumentSerializer.Meta):
        fields = DocumentSerializer.Meta.fields + \
                ('approved_clauses', 'pending_clauses')

    def get_approved_clauses(self, instance):
        return instance.approved_clauses

    def get_pending_clauses(self, instance):
        return instance.pending_clauses

