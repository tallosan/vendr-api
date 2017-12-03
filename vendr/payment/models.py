#
# Payments API.
#
# @author :: tallosanI
# ================================================================

from __future__ import unicode_literals

import uuid
import json

import requests
from requests.auth import HTTPBasicAuth

from django.db import models
from django.conf import settings

from transaction.models import Transaction


def SET_NAME(collector, field, sub_objs, using):
    """
    Custom `on_delete` field. Sets the payment model's user fields
    to the user's full name on deletion.
    """
    
    _field_name = str(field).split(".")[-1]
    _payment = sub_objs[0]

    kuser = getattr(_payment, _field_name)
    user_name = kuser.full_name

    collector.add_field_update(
            field,
            user_name,
            sub_objs
    )


class PaymentAdapterInterface(object):
    """
    Defines an interface for payment adapters.
    """

    BASE_URL = ""

    def create_payment(self, payment):
        """
        Create a payment using the given payment.
        """
        raise NotImplementedError("error: all adapters must implement this.")

    def _format_request(self, payment):
        """
        Format a request from the given payment.
        """
        raise NotImplementedError("error: all adapters must implement this.")


class VersaPayAdapter(PaymentAdapterInterface):
    """
    Payment adapter for VersaPay.
    """

    BASE_URL = "https://demo.versapay.com"

    def create_payment(self, payment):
        """
        Create a payment using the given payment.
        """

        create_url = "{}/api/transactions".format(self.BASE_URL)

        api_token = "GLCbtpMHVWwctcfNxDVw"
        api_key = "yce6_WgurFnts8r1my8n"

        payment_data = self._format_request(payment)
        print payment_data

        # Send the request, and ensure that it went through successfully.
        request = requests.post(
                create_url,
                data=payment_data,
                auth=HTTPBasicAuth(api_token, api_key)
        )

        print request.text
        assert request.status_code == 201, (
                "error: this payment failed to go through, and returned "
                "a status code of {}".format(request.status_code)
        )

    def _format_request(self, payment):
        """
        Format a request from the given payment for the VersaPay API. Two
        key things to note here -- firstly, VersaPay requires the amount to be
        in cents, and secondly, VersaPay requests require a transaction type. As
        we're always sending requests, we can hardcode this to "send".
        """

        recipient_email = payment.recipient.email
        amount_in_cents = payment.amount * 100
        transaction_type = "request"

        payment_data = json.dumps({
                "email": recipient_email,
                "amount_in_cents": amount_in_cents,
                "transaction_type": transaction_type,
                "message": payment.message
        })

        return payment_data


class Payment(models.Model):
    """
    Represents a payment in the system, from one user to another.
    Fields:
        `payee` (KUser) -- The user making the payment.
        `recipient` (KUser) -- The user receiving the payment.
        `transaction` (Transaction) -- The transaction this payment is being
            made on.
        `amount` (float) -- The payment amount.
        `message` (str) -- An optional message from the payee to recipient.
        `timestamp` (date) -- The date the payment was made.
        `_payee` (str) -- The user's name. Used for historical purposes.
        `_recipient` (str) -- The user's name. Used for historical purposes.
        `payment_adapter` (adapter) -- An adapter for a payment API.
    """
    
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            db_index=True
    )

    payee = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name="payee",
            db_index=True,
            on_delete=SET_NAME
    )
    recipient = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name="recipient",
            db_index=True,
            on_delete=SET_NAME
    )
    transaction = models.ForeignKey(
            Transaction,
            related_name="transaction",
            db_index=True,
            on_delete=models.SET_NULL,
            null=True
    )

    amount = models.FloatField()
    message = models.CharField(max_length=140, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    _payee = models.CharField(max_length=64, default=None, null=True)
    _recipient = models.CharField(max_length=64, default=None, null=True)

    payment_adapter = VersaPayAdapter()

    def save(self, *args, **kwargs):
        """
        On Payment creation, send the given amount from the payee's account
        to the recipient's.
        """

        if self._state.adding:
            self.send_payment(
                    self.payee, 
                    self.recipient, 
                    self.transaction, 
                    self.amount
            )

    def send_payment(self, payee, recipient, transaction, amount):
        """
        Send the given amount from the payee's account to the recipient's.
        Args:
            `payee` (KUser) -- The user making the payment.
            `recipient` (KUser) -- The user receiving the payment.
            `transaction` (Transaction) -- The transaction this payment is being
                made on.
            `amount` (float) -- The payment amount.
            `timestamp` (date) -- The date the payment was made.
        """

        # TODO: Assert both users have accounts.
        self.payment_adapter.create_payment(self)

