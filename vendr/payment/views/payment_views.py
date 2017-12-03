#
# Payments API.
#
# @author :: tallosanI
# ================================================================

from rest_framework import status
from rest_framework.generics import (CreateAPIView, RetrieveUpdateAPIView)
from rest_framework.response import Response

from payment.models import Payment
from payment.serializers import PaymentSerializer


class PaymentList(CreateAPIView):
    
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request, format=None):

        payee = request.user
        assert payee, (
                "error: no payee given."
        )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(payee=payee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetail(RetrieveUpdateAPIView):
    pass

