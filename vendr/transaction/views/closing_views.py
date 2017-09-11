#
# Closing views.
#
# ======================================================================

from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import generics, status, permissions
from rest_framework.generics import *

from vendr_core.generics import NestedListAPIView, NestedListCreateAPIView, \
        NestedListUpdateAPIView, NestedRetrieveUpdateDestroyAPIView, \
        NestedUpdateAPIView

from transaction.models import Transaction, Closing, Amendments, Waiver, \
        NoticeOfFulfillment, MutualRelease, DocumentClause, \
        StaticClause, DynamicClause
from transaction.serializers import ClosingSerializer, DocumentSerializer, \
        ClauseDocumentSerializer, DocumentClauseSerializer
import transaction.permissions as transaction_permissions


User = get_user_model()


class ClosingDetail(NestedListUpdateAPIView):
    
    parent = Transaction
    parent_pk_field = 'transaction_pk'
    parent_field_name = 'transaction'
    field_name = 'closing'

    pagination_class = None
    queryset = Closing.objects.all()
    serializer_class = ClosingSerializer
    permission_classes = ( permissions.IsAuthenticated, )


class ClosingDetail(NestedRetrieveUpdateDestroyAPIView):
    
    parent = Transaction
    parent_pk_field = 'transaction_pk'
    field_name = 'closing'
    pk_field = 'closing_pk'

    queryset = Closing.objects.all()
    serializer_class = ClosingSerializer
    permission_classes = ( permissions.IsAuthenticated, )


class OneToOneMixin(GenericAPIView):
    
    """ View used for nested one-to-one objects.
        Attributes:
            `root_parent` (str) -- The first parent object with an ID.
            `root_pk` (str) -- The parent's PK field.
            `model_tree` (list of tuples) -- A list of all the models in the tree. 

        Examples:

            parent/<parent_pk>/first-model/second-model/<second_model_pk>/target/

            self.root_parent = Parent
            self.root_pk = 'parent_pk'
            self.model_tree = [
                (first_model, None),
                (second_model, 'second_model_pk'),
                (target, None)
            ]
    """

    """ Traverse the model tree until we arrive at the target nested
        model's parent. Note, this will be the second last object
        in `self.model_tree`. """
    def _get_parent(self):

        parent = self.root_parent.objects.get(pk=self.kwargs[self.root_pk])
        class_name, pk_field = 0, 1
        for model in self.model_tree[:-1]:
            parent = getattr(parent, model[class_name], None)
            assert parent, (
                    'nested model {} cannot be found'
            ).format(model[class_name])

            if model[pk_field]:
                nested_model = parent.objects.get(self.kwargs[model[pk_field]])

        return parent

    """ Get the model queryset. """
    def get_queryset(self):

        parent = self._get_parent()
        self.check_object_permissions(self.request, parent)
        nested_queryset = getattr(parent, self.model_tree[-1][0])
        if hasattr(nested_queryset, 'all'):
            return nested_queryset.all()

        return [nested_queryset]

    """ Step through the model heirarchy. """
    def get_object(self):
        
        try:
            nested_parent = self._get_parent()
            nested_set = getattr(nested_parent, self.model_tree[-1][0])
            instance = nested_set.get(pk=self.kwargs[self.pk])
            self.check_object_permissions(self.request, instance)
            return instance

        except nested_set.model.DoesNotExist:
            error_msg = {'error': 'nested model with pk {} does not exist.'.\
                    format(self.kwargs[self.pk])}
            dne_exc = APIException(detail=error_msg)
            dne_exc.status_code = 404; raise dne_exc


class DocumentClauseCreateMixin(object):
        
    def post(self, request, *args, **kwargs):

        document = self._get_parent()
        parent_field_name = 'document'

        # Get the Clause ID, and the actual clause object.
        contract = document.closing.transaction.contracts.all()[0]
        if 'clause' not in request.data.keys():
            error_msg = {'error': '`clause` must be provided.'}
            dne_exc = APIException(detail=error_msg)
            dne_exc.status_code = 401; raise dne_exc

        clause_pk = request.data.pop('clause')
        try:
            clause = contract.static_clauses.get(pk=clause_pk)
        except StaticClause.DoesNotExist:
            try:
                clause = contract.dynamic_clauses.get(pk=clause_pk)
            except DynamicClause.DoesNotExist:
                error_msg = {"error": "clause with pk {} does not exist in "
                             "the transaction's contract.".format(clause_pk)}
                dne_exc = APIException(detail=error_msg)
                dne_exc.status_code = 404; raise dne_exc

        # Create the serializer. Note, we need to check for duplicates here.
        serializer = self.get_serializer(data=request.data, context=request.FILES)
        if serializer.is_valid():
            try:
                serializer.save(**{parent_field_name: document,
                    'clause': clause, 'sender': request.user}
                )
            except ValueError as value_error:
                error_msg = {'error': str(value_error)}
                duplicate_exc = APIException(detail=error_msg)
                duplicate_exc.status_code = 400; raise duplicate_exc

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AmendmentsList(OneToOneMixin, NestedListUpdateAPIView):

    root_parent = Transaction
    root_pk = 'transaction_pk'
    model_tree = [
            ('closing', None),
            ('amendments', None)
    ]

    serializer_class = ClauseDocumentSerializer
    permission_classes = ( permissions.IsAuthenticated, )
    
    
class AmendmentsClauseList(DocumentClauseCreateMixin, OneToOneMixin, ListAPIView):

    root_parent = Transaction
    root_pk = 'transaction_pk'
    model_tree = [
            ('closing', None),
            ('amendments', None),
            ('document_clauses', None)
    ]

    serializer_class = DocumentClauseSerializer
    permission_classes = (
            permissions.IsAuthenticated,
            transaction_permissions.ClauseDocumentListPermissions
    )


class AmendmentsClauseDetail(OneToOneMixin, RetrieveUpdateAPIView):

    root_parent = Transaction
    root_pk = 'transaction_pk'
    pk = 'pk'
    model_tree = [
            ('closing', None),
            ('amendments', None),
            ('document_clauses', None)
    ]

    serializer_class = DocumentClauseSerializer
    permission_classes = ( 
            permissions.IsAuthenticated,
            transaction_permissions.ClauseDocumentDetailPermissions
    )


class WaiverList(OneToOneMixin, NestedListCreateAPIView):

    root_parent = Transaction
    root_pk = 'transaction_pk'
    model_tree = [
            ('closing', None),
            ('waiver', None)
    ]

    serializer_class = ClauseDocumentSerializer
    permission_classes = ( permissions.IsAuthenticated, )


class WaiverClauseList(DocumentClauseCreateMixin, OneToOneMixin, ListAPIView):

    root_parent = Transaction
    root_pk = 'transaction_pk'
    model_tree = [
            ('closing', None),
            ('waiver', None),
            ('document_clauses', None)
    ]

    serializer_class = DocumentClauseSerializer
    permission_classes = (
            permissions.IsAuthenticated,
            transaction_permissions.ClauseDocumentListPermissions
    )


class WaiverClauseDetail(OneToOneMixin, RetrieveUpdateAPIView):

    root_parent = Transaction
    root_pk = 'transaction_pk'
    pk = 'pk'
    model_tree = [
            ('closing', None),
            ('waiver', None),
            ('document_clauses', None)
    ]

    serializer_class = DocumentClauseSerializer
    permission_classes = ( 
            permissions.IsAuthenticated,
            transaction_permissions.ClauseDocumentDetailPermissions
    )


class NoticeOfFulfillmentList(OneToOneMixin, NestedListCreateAPIView):

    root_parent = Transaction
    root_pk = 'transaction_pk'
    model_tree = [
            ('closing', None),
            ('notice_of_fulfillment', None)
    ]

    serializer_class = ClauseDocumentSerializer
    permission_classes = ( permissions.IsAuthenticated, )


class NoticeOfFulfillmentClauseList(OneToOneMixin, ListAPIView):

    root_parent = Transaction
    root_pk = 'transaction_pk'
    model_tree = [
            ('closing', None),
            ('notice_of_fulfillment', None),
            ('document_clauses', None)
    ]

    serializer_class = DocumentClauseSerializer
    permission_classes = (
            permissions.IsAuthenticated,
            transaction_permissions.ClauseDocumentListPermissions
    )


class NoticeOfFulfillmentClauseDetail(OneToOneMixin, RetrieveUpdateAPIView):

    root_parent = Transaction
    root_pk = 'transaction_pk'
    pk = 'pk'
    model_tree = [
            ('closing', None),
            ('notice_of_fulfillment', None),
            ('document_clauses', None)
    ]

    serializer_class = DocumentClauseSerializer
    permission_classes = ( 
            permissions.IsAuthenticated,
            transaction_permissions.ClauseDocumentDetailPermissions
    )


class MutualReleaseList(OneToOneMixin, NestedListCreateAPIView):

    root_parent = Transaction
    root_pk = 'transaction_pk'
    model_tree = [
            ('closing', None),
            ('mutual_release', None),
    ]

    queryset = MutualRelease.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )

