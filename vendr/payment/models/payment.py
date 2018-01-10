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

    def deposit(self, payment):
        """
        Deposit a payment to VenDoor.
        """
        raise NotImplementedError("error: all adapters must implement this.")

    def forward(self, recipient):
        """
        Forward a payment from VenDoor.
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

    def deposit(self, payment):
        """
        Deposit a payment to VenDoor.
        Args:
            `payment` (Payment) -- The Payment to be deposited.
        """

        create_url = "{}/api/transactions".format(self.BASE_URL)

        api_token = "mH6KaxxNud9tUghmHdfL"
        api_key = "V5fk96tHMyNvsZyYH5WJ"

        # Send the request, and ensure that it went through successfully.
        payment_data = self._format_request(payment)
        request = requests.post(
                create_url,
                data=payment_data,
                auth=HTTPBasicAuth(api_token, api_key)
        )

        assert request.status_code == 201, (
                "error: this payment failed to go through, and returned "
                "a status code of {}".format(request.status_code)
        )

        return request.status_code

    def forward(self, recipient):
        """
        Forward a payment from VenDoor.
        Args:
            `recipient` (User) -- The recipient of this payment forwarding.
        """

    def _format_request(self, payment):
        """
        Format a request from the given payment for the VersaPay API. Two
        key things to note here -- firstly, VersaPay requires the amount to be
        in cents, and secondly, VersaPay requests require a transaction type.
        """

        amount_in_cents = payment.amount * 100

        # Convert the payment type accordingly.
        conv_type = lambda t: "direct_credit" if t == "DEBIT" else "direct_debit"
        transaction_type = conv_type(payment._payment_type)
        payment_data = {
                "amount_in_cents": amount_in_cents,
                "transaction_type": transaction_type,
                "email": settings.PAYMENT_EMAIL,
                "fund_token": settings.PAYMENT_FUND_TOKEN,
                "institution_number": settings.PAYMENT_INSTITUTION_NUMBER,
                "branch_number": settings.PAYMENT_BRANCH_NUMBER,
                "account_number": settings.PAYMENT_ACCOUNT_NUMBER,
                "message": payment.message,
                "memo": "WaiHome memo",
                "business_name": "WaiHome",
        }

        return payment_data


class Payment(models.Model):
    """
    Represents a payment in the VenDoor system. There are essentially three
    parties in the transaction -- VenDoor, the payee, and the recipient. Thus,
    we have three separate bank accounts for each. The VenDoor details are
    saved in our `settings` file, whereas the user's details are provided on
    payment creation.

    Payment Lifecycle:

    - Firstly, the buyer sends an EFT deposit to our (VenDoor) account.
    - We subsequently will act as an escrow service, and hold this deposit
      until the transaction completes.
    - If the transaction is successful, then the deposit is forwarded on to
      the seller at the agreed upon time (see contract).
    - If not, we'll return all the funds back to the buyer.

    Fields:
        `payee` (KUser) -- The user making the payment.
        `recipient` (KUser) -- The user receiving the payment.
        `transaction` (Transaction) -- The transaction this payment is being
            made on.
        `amount` (float) -- The payment amount.
        `message` (str) -- An optional message from the payee to recipient.
        `*_bank` (str) -- The user's bank name (e.g. BMO).
        `*_insitution_number` (str) -- The user's institution number.
        `*_branch_number` (str) -- The user's bank branch number.
        `*_account_number` (str) -- The user's bank account number.
        `_payee` (str) -- The user's name. Used for historical purposes.
        `_recipient` (str) -- The user's name. Used for historical purposes.
        `timestamp` (date) -- The date the payment was made.
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
            on_delete=models.SET_NULL,
            null=True
    )
    recipient = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name="recipient",
            db_index=True,
            on_delete=models.SET_NULL,
            null=True
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

    """
    # Payee banking details.
    payee_bank = models.CharField(max_length=64)
    payee_insitution_number = models.CharField(max_length=3)
    payee_branch_number = models.CharField(max_length=5)
    payee_account_number = models.CharField(max_length=12)

    # Recipient banking details.
    recipient_bank = models.CharField(max_length=64)
    recipient_insitution_number = models.CharField(max_length=3)
    recipient_branch_number = models.CharField(max_length=5)
    recipient_account_number = models.CharField(max_length=12)

    # Meta details.
    _payee = models.CharField(max_length=64, default=None, null=True)
    _recipient = models.CharField(max_length=64, default=None, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    """
    payment_adapter = VersaPayAdapter()

    def save(self, *args, **kwargs):
        """
        On Payment creation, we need to send the given amount from the
        payee's account to the recipient's.
        """

        if self._state.adding:
            self.deposit()

            self._payee = self.payee.full_name
            self._recipient = self.recipient.full_name

        super(Payment, self).save(*args, **kwargs)

    def deposit(self):
        """
        Deposit the payment into a VenDoor account. This is the first step
        in the payment lifecycle.
        """

        self.payment_adapter.deposit(self)

    def forward(self, recipient):
        """
        Forward the payment from a VenDoor account, where it has been held
        in escrow, to the target recipient. The recipient is designated
        according to the state of the transaction. If it was successful, then
        we'll send it on to the seller. If not, we'll return the funds to
        the buyer.
        Args:
            `recipient` (User) -- The recipient for this payment.
        """

        self.payment_adapter.forward(self)

