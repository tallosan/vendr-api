#
# User schedule.
#
# =========================================================================

from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

from vendr_core.permissions import IsOwner

from kuser.serializers import UserContractSerializer


User = get_user_model()


class ContractList(RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserContractSerializer
    permission_classes = ( permissions.IsAuthenticated, IsOwner )

    def get(self, request, *args, **kwargs):

        self.check_object_permissions(request, self)
        return super(ContractList, self).get(request, *args, **kwargs)

