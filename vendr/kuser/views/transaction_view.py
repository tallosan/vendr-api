#
# User schedule.
#
# =========================================================================

from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

from vendr_core.permissions import IsOwner

from kuser.serializers import UserTransactionSerializer


User = get_user_model()


class TransactionList(RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserTransactionSerializer

