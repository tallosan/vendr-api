#
# Payment sub-views.
#
# @author :: tallosan
# ================================================================

from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView

from django.contrib.auth import get_user_model

from kuser.serializers import PaymentSerializer
from vendr_core.permissions import IsOwner

User = get_user_model()


class PaymentList(RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = ( permissions.IsAuthenticated, IsOwner )

