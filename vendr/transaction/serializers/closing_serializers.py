#
# Closing stage serializers.
#
# ===========================================================================


from django.conf import settings

from rest_framework import serializers

from transaction.models import Closing, Document, DocumentClause, \
        AmendmentDocumentTextClause, AmendmentDocumentToggleClause, \
        AmendmentDocumentChipClause, AmendmentDocumentDateClause, \
        AmendmentDocumentClause


class ClosingSerializer(serializers.ModelSerializer):
    
    transaction = serializers.ReadOnlyField(source='transaction.pk')
    buyer = serializers.ReadOnlyField(source='transaction.buyer.pk')
    seller = serializers.ReadOnlyField(source='transaction.seller.pk')
    
    class Meta:
        model = Closing
        fields = (
                'pk',
                'transaction',
                'buyer',
                'seller',
                '_property_descriptor',
                '_document_header',
                '_document_footer'
        )


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('pk', 'title', 'content', 'explanation', 'signing_date')


class DocumentClauseSerializer(serializers.ModelSerializer):

    title = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()
    generator = serializers.SerializerMethodField()
    waived = serializers.SerializerMethodField()

    class Meta:
        model = DocumentClause
        fields = (
                'pk',
                'buyer_accepted',
                'seller_accepted',
                'title',
                'preview',
                'generator',
                'waived',
                'timestamp'
        )

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

    """ Returns the title of the `DocumentClause` clause.
        Args:
            instance (DocumentClause) -- The `DocumentClause` being serialized.
    """
    def get_title(self, instance):
        return instance.title

    """ Returns the preview of the `DocumentClause` clause.
        Args:
            instance (DocumentClause) -- The `DocumentClause` being serialized.
    """
    def get_preview(self, instance):
        return instance.clause.preview

    """ Returns the generator of the `DocumentClause` clause.
        Args:
            instance (DocumentClause) -- The `DocumentClause` being serialized.
    """
    def get_generator(self, instance):

        try:
            generator = instance.clause.generator
        except AttributeError:
            generator = None

        return generator

    """ Returns the `waived` status of the `DocumentClause`
        Args:
            instance (DocumentClause) -- The `DocumentClause` being serialized.
    """
    def get_waived(self, instance):
        return instance.clause._waived


class AmendmentClauseSerializer(DocumentClauseSerializer):

    amendment = serializers.SerializerMethodField()

    class Meta(DocumentClauseSerializer.Meta):
        model = AmendmentDocumentClause
        fields = DocumentClauseSerializer.Meta.fields + ('amendment', )

    """ Get the amendment value for this serializer. We're using a method
        field in order to maintaing the psuedo-generic property that allows
        us to use the same serializer for all AmendmentDocumentClause's.
    """
    def get_amendment(self, instance):

        if isinstance(instance, DocumentClause):
            instance = instance.amendmentdocumentclause

        # Downcast.
        if hasattr(instance, 'amendmentdocumenttoggleclause'):
            instance = instance.amendmentdocumenttoggleclause
        elif hasattr(instance, 'amendmentdocumentdateclause'):
            instance = instance.amendmentdocumentdateclause 
        elif hasattr(instance, 'amendmentdocumentchipclause'):
            instance = instance.amendmentdocumentchipclause
        else: 
            instance = instance.amendmentdocumenttextclause

        return instance.amendment

    def create(self, validated_data):

        document = validated_data.pop('document')
        clause = validated_data.pop('clause')
        sender = validated_data.pop('sender')
        amendment = validated_data.pop('amendment')

        document_clause = document.add_clause(clause, sender=sender,
                amendment=amendment)
        return document_clause

    """ This is a bit hacky, but it allows us to get access to the
        full response data, as opposed to the filtered / validated
        data that Django will return naturally.
    """
    def to_internal_value(self, data):
        return data


class ClauseDocumentSerializer(DocumentSerializer):

    approved_clauses = serializers.SerializerMethodField()
    pending_clauses = serializers.SerializerMethodField()
    rejected_clauses = serializers.SerializerMethodField()

    # The serializer to use on the document's clauses.
    _clause_serializer = DocumentClauseSerializer

    class Meta(DocumentSerializer.Meta):
        fields = DocumentSerializer.Meta.fields + \
                ('approved_clauses', 'pending_clauses', 'rejected_clauses')

    """ Set of approved clauses on this Document.
        Args:
            instance (ClauseDocument) -- The document being serialized.
    """
    def get_approved_clauses(self, instance):
        
        return self._clause_serializer(
                instance.approved_clauses,
                many=True
        ).data

    """ Set of pending clauses on this Document.
        Args:
            instance (ClauseDocument) -- The document being serialized.
    """
    def get_pending_clauses(self, instance):
        
        return self._clause_serializer(
                instance.pending_clauses,
                many=True
        ).data

    """ Set of rejected clauses on this Document.
        Args:
            instance (ClauseDocument) -- The document being serialized.
    """
    def get_rejected_clauses(self, instance):
        
        return self._clause_serializer(
                instance.rejected_clauses,
                many=True
        ).data


class AmendmentClauseDocumentSerializer(ClauseDocumentSerializer):
    _clause_serializer = AmendmentClauseSerializer

