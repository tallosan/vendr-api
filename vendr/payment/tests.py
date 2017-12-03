#
# Payments API test suite.
#
# @author :: tallosanI
# ================================================================

from django.test import TestCase

from rest_framework import status
from rest_framework.test import (
        APIRequestFactory, APIClient, APITestCase, force_authenticate
)

from kuser.models import KUser as User
from payment.models import *
from payment.views import PaymentList


class TestPaymentsList(APITestCase):

    def setUp(self):

        self.view = PaymentList.as_view()
        self.factory = APIRequestFactory()
 
        # Create the buyer, and seller.
        self.payee = User.objects.create_user(
                email="payee@vendoor.ca",
                phone_num='7782304056',
                password='payee'
        )
        self.recipient = User.objects.create_user(
                email="recipient@vendoor.ca",
                phone_num='7782304056',
                password='recipient'
        )

        self.path = '/v1/payments/'

    def test_create_payment(self):
        """
        Ensure that we can create payments.
        """
        
        payment_data = {
                "amount": 1,
                "recipient": self.recipient.pk,
                "message": "Hello, world."
        }

        request = self.factory.post(self.path, payment_data, format="json")
        force_authenticate(request, self.payee)
        response = self.view(request)

        self.assertEqual(response.status_code, 201)

