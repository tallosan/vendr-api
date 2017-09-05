#
# Closing stage serializers.
#
# ===========================================================================


from django.conf import settings

from rest_framework import serializers

from transaction.models import Closing, Document, DocumentClause


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


class DocumentClauseSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()

    class Meta:
        model = DocumentClause
        fields = ('pk', 'title', 'buyer_accepted', 'seller_accepted')

    """ Returns the title of the `DocumentClause` title.
        Args:
            instance (DocumentClause) -- The `DocumentClause` being serialized.
    """
    def get_title(self, instance):
        return instance.clause.title


class ClauseDocumentSerializer(DocumentSerializer):

    approved_clauses = serializers.SerializerMethodField()
    pending_clauses = serializers.SerializerMethodField()

    class Meta(DocumentSerializer.Meta):
        fields = DocumentSerializer.Meta.fields + \
                ('approved_clauses', 'pending_clauses')

    """ Set of approved clauses on this Document.
        Args:
            instance (ClauseDocument) -- The document being serialized.
    """
    def get_approved_clauses(self, instance):
        return {
                "approved_clauses": DocumentClauseSerializer(
                 instance.approved_clauses, many=True).data
        }

    """ Set of pending clauses on this Document.
        Args:
            instance (ClauseDocument) -- The document being serialized.
    """
    def get_pending_clauses(self, instance):
        return {
                "pending_clauses": DocumentClauseSerializer(
                 instance.pending_clauses, many=True).data
        }

