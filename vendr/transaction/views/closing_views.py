#
# Closing views.
#
# ======================================================================

from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions

from vendr_core.generics import NestedListAPIView, NestedListCreateAPIView, \
        NestedRetrieveUpdateDestroyAPIView

from transaction.models import Transaction, Closing, Amendments, Waiver, \
        NoticeOfFulfillment, MutualRelease
from transaction.serializers import ClosingSerializer, DocumentSerializer, \
        ClauseDocumentSerializer

User = get_user_model()


class ClosingList(NestedListAPIView):
    
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


class AmendmentsList(NestedListCreateAPIView):

    parent = Closing
    parent_pk_field = 'closing_pk'
    parent_field_name = 'closing'
    field_name = 'amendments'

    queryset = Amendments.objects.all()
    serializer_class = ClauseDocumentSerializer
    permission_classes = ( permissions.IsAuthenticated, )


class WaiverList(NestedListCreateAPIView):

    parent = Closing
    parent_pk_field = 'closing_pk'
    parent_field_name = 'closing'
    field_name = 'waiver'

    queryset = Waiver.objects.all()
    serializer_class = ClauseDocumentSerializer
    permission_classes = ( permissions.IsAuthenticated, )


class NoticeOfFulfillmentList(NestedListCreateAPIView):

    parent = Closing
    parent_pk_field = 'closing_pk'
    parent_field_name = 'closing'
    field_name = 'notice_of_fulfillment'

    queryset = NoticeOfFulfillment.objects.all()
    serializer_class = ClauseDocumentSerializer
    permission_classes = ( permissions.IsAuthenticated, )


class MutualReleaseList(NestedListCreateAPIView):

    parent = Closing
    parent_pk_field = 'closing_pk'
    parent_field_name = 'closing'
    field_name = 'mutual_release'

    queryset = MutualRelease.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = ( permissions.IsAuthenticated, )

