#
# Payments API.
#
# @author :: tallosan
# ================================================================

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
        CreateAPIView,
        RetrieveUpdateDestroyAPIView
)

from kuser.models import BaseAccount
from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentList(CreateAPIView):
    
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):

        payee = request.user
        assert payee, (
                "error: no payee given."
        )

        request.data["payee"] = payee.pk
        return super(PaymentList, self).post(request, *args, **kwargs)


class PaymentDetail(RetrieveUpdateDestroyAPIView):
    
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_url_kwarg = "payment_pk"

    def update(self, request, *args, **kwargs):
        """
        Override to allow partial updates.
        """

        kwargs["partial"] = True
        return super(PaymentDetail, self).update(request, *args, **kwargs)

