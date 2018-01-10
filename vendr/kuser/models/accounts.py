#
# Financial accounts API.
#
# @author :: tallosan
# ================================================================

import uuid

from django.db import models
from django.conf import settings


class AbstractAccountFactory(object):
    """
    Abstract factory for account creation.
    """

    def create_account(self, owner, account_type, account_data):
        """
        Create the account corresponding to the given account type.
        Args:
            `account_type` (str) -- The account type to create.
        """

        # Select the appropriate account factory, and create the
        # corresponding account.
        if account_type == "bank":
            factory = BankAccount.objects
        else:
            raise ValueError("error: `account_type` is not valid.")

        account = factory.create(owner=owner, **account_data)
        return account


class BaseAccount(models.Model):
    """
    Base account for all account types (debit, chequing, etc).
    """

    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            db_index=True
    )

    owner = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name="accounts",
            on_delete=models.CASCADE
    )


class BankAccount(BaseAccount):
    """
    A user's bank account.
    Fields:
        `bank` (str) -- The user's bank name (e.g. BMO).
        `insitution_number` (str) -- The user's institution number.
        `branch_number` (str) -- The user's bank branch number.
        `account_number` (str) -- The user's bank account number
    """

    bank = models.CharField(max_length=64)
    insitution_number = models.CharField(max_length=3)
    branch_number = models.CharField(max_length=5)
    account_number = models.CharField(max_length=12)

