#
# Closing stage serializers.
#
# ===========================================================================


from django.conf import settings

from rest_framework import serializers

from transaction.models import Closing, Document, DocumentClause, \
        AmendmentDocumentClause


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
    waived = serializers.SerializerMethodField()

    class Meta:
        model = DocumentClause
        fields = ('pk', 'title', 'buyer_accepted', 'seller_accepted', 'waived')

    """ We're overiding this function to use our `add_clause()` method.
        Args:
            validated_data (OrderedDict) -- The POST request data.
    """
    def create(self, validated_data):

        document = validated_data.pop('document')
        clause = validated_data.pop('clause')
        sender = validated_data.pop('sender')

        document_clause = document.add_clause(clause, sender=sender)

        return document_clause

    """ Returns the title of the `DocumentClause` title.
        Args:
            instance (DocumentClause) -- The `DocumentClause` being serialized.
    """
    def get_title(self, instance):
        return instance.title

    """ Returns the `waived` status of the `DocumentClause`
        Args:
            instance (DocumentClause) -- The `DocumentClause` being serialized.
    """
    def get_waived(self, instance):
        return instance.clause._waived

    def to_representation(self, instance):

        document_clause = super(DocumentClauseSerializer, self).\
                to_representation(instance)
        try:
            document_clause['generator'] = instance.clause.generator
        except AttributeError: pass

        return document_clause


class AmendmentClauseSerializer(DocumentClauseSerializer):

    class Meta(DocumentClauseSerializer.Meta):
        model = AmendmentDocumentClause
        fields = DocumentClauseSerializer.Meta.fields + ('amendment', )

    def create(self, validated_data):

        document = validated_data.pop('document')
        clause = validated_data.pop('clause')
        sender = validated_data.pop('sender')
        amendment = validated_data.pop('amendment')

        document_clause = document.add_clause(clause, sender=sender,
                amendment=amendment)
        return document_clause

    def to_representation(self, instance):
        instance = instance.amendmentdocumentclause
        return super(AmendmentClauseSerializer, self).to_representation(instance)


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

