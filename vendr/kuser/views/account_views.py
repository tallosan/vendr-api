#
# Account views.
#
# @author :: tallosan
# ================================================================

from rest_framework import status
from rest_framework.generics import (
        ListCreateAPIView,
        RetrieveUpdateDestroyAPIView
)

from kuser.models import BaseAccount, AbstractAccountFactory
from kuser.serializers import (
        GenericAccountSerializer, BankAccountSerializer
)

from vendr_core.permissions import IsOwner


class AccountList(ListCreateAPIView):

    # TODO: Implement LIST view function.

    queryset = BaseAccount.objects.all()
    permission_classes = (IsOwner, )
    _mapping = {
            "generic": GenericAccountSerializer,
            "bank": BankAccountSerializer
    }

    def get_serializer_class(self):
        """
        Return the appropriate serializer for any model changes, and
        the generic for any read operations.
        """

        account_type = "generic"
        if self.request.method == "POST":
            account_type = self.request.data.get("account_type")

        return self._mapping[account_type]
    
    def post(self, request, *args, **kwargs):

        account_type = request.data.get("account_type", None)
        assert account_type, (
                "error: `account_type` must be specified."
        )

        request.data["owner"] = request.user.pk
        return super(AccountList, self).post(request, *args, **kwargs)


class AccountDetail(RetrieveUpdateDestroyAPIView):

    queryset = BaseAccount.objects.all()
    permission_classes = (IsOwner, )
    lookup_url_kwarg = "account_pk"
    _mapping = {
            "bank": BankAccountSerializer
    }

    _instance_type = None

    def get_object(self):
        """
        Override to set the `_instance_type` field. This will allow
        us to serialize `Account` models dynamically.
        """

        instance = super(AccountDetail, self).get_object()
        if hasattr(instance, "bankaccount"):
            instance = instance.bankaccount
            self._instance_type = "bank"
        else:
            raise ValueError("error: instance has invalid type.")

        return instance

    def get_serializer_class(self):
        return self._mapping[self._instance_type]

    def update(self, request, *args, **kwargs):
        """
        Override to allow partial updates.
        """

        kwargs["partial"] = True
        return super(AccountDetail, self).update(request, *args, **kwargs)

