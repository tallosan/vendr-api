#
# Closing views.
#
# ======================================================================

from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions

from vendr_core.mixins import NestedListCreateModelMixin, \
        NestedRetrieveUpdateDestroyAPIView

User = get_user_model()


class ClosingDetail(APIView):
    pass


class AmendmentsList(APIView):
    pass


class WaiverList(APIView):
    pass


class NoticeOfFulfillmentList(APIView):
    pass


class MutualReleaseList(APIView):
    pass

