from __future__ import unicode_literals

import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone

from model_utils.managers import InheritanceManager

from kproperty.models import Property
from .closing import AbstractClosingFactory


class TransactionManager(models.Manager):
    """
    Custom Transaction Manager.
    """
    
    def create_transaction(self, buyer, seller, kproperty, **extra_fields):
        """
        Creates a Transaction model, along with the given Contract.
        Args:
            `buyer` (KUser) -- The User who wants to buy the property. 
            `seller` (KUser) -- The User who is selling the property.
            `kproperty` (Property) -- The Property the transaction is on.
        """

        # Ensure that the buyer, seller, and property are specified.
        if any(arg is None for arg in {buyer, seller, kproperty}):
            raise ValueError('buyer, seller, or kproperty not specified.')
        
        # Ensure that the seller actually owns the property.
        if seller.id != kproperty.owner.id:
            raise ValueError('seller id does not match property owner id.')
        
        # Ensure that the user is not starting a transaction on their own property.
        if seller.pk == buyer.pk:
            raise ValueError("transaction cannot created on user's own property.")

        # Create the transaction.
        now = timezone.now()
        transaction = self.create(buyer=buyer, seller=seller, kproperty=kproperty,
                        start_date=now, **extra_fields
        )

        return transaction


class Transaction(models.Model):
    """
    Transaction model. Each Transaction has a buyer, a seller, and a property, along 
    with a set of Offers and a Contract. Each Transaction has 3 stages.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
            editable=False, db_index=True)
    
    # The buyer, seller, and the property this transaction is on.
    buyer = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='buyer',
            editable=False,
            on_delete=models.CASCADE,
            db_index=True
    )
    seller = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            related_name='seller',
            editable=False,
            on_delete=models.CASCADE,
            db_index=True
    )
    kproperty = models.ForeignKey(
            Property,
            related_name='kproperty',
            editable=False,
            on_delete=models.CASCADE,
            db_index=True
    )

    buyer_accepted_offer  = models.UUIDField(blank=True, null=True)
    seller_accepted_offer = models.UUIDField(blank=True, null=True)
    
    contracts_equal = models.BooleanField(default=False)
    buyer_accepted_contract  = models.BooleanField(default=False)
    seller_accepted_contract = models.BooleanField(default=False)

    payment = models.ForeignKey(
            "payment.Payment",
            related_name="payment",
            on_delete=models.SET_NULL,
            db_index=True,
            null=True
    )

    # The transaction stage we"re in.
    STAGES = (
            (0, "OFFER_STAGE"),
            (1, "NEGOTIATION_STAGE"),
            (2, "CLOSING_STAGE")
    )
    stage = models.IntegerField(choices=STAGES, default=0)
    start_date = models.DateTimeField(auto_now_add=True)
    
    # Signal handler.
    _dampen = models.BooleanField(default=False)
    _fired  = models.BooleanField(default=False)
    
    objects = TransactionManager()

    class Meta:
        unique_together = ["buyer", "seller", "kproperty"]

    def check_field_permissions(self, user_id, fields):
        """
        Returns True if the user has permission to access the given fields,
        and False if not.
        Args:
            user_id: The ID of the User.
            fields: The fields the User is attempting to modify.
        """

        # Mapping between users and the restricted fields that
        # they cannot access.
        restricted_fields = {
                self.buyer.pk: [
                    "seller_accepted_offer",
                    "seller_accepted_contract",
                    "contracts_equal"
                ],
                self.seller.pk: [
                    "buyer_accepted_offer",
                    "buyer_accepted_contract",
                    "contracts_equal"
                ]
        }
        
        # Return False if a field is not in the user's permission scope.
        for field in fields:
            if field in restricted_fields[user_id]:
                return False

        return True

    def advance_stage(self):
        """
        Advance the transaction to the next stage. This is really just a bunch of
        conditionals that need to be passed depending on the stage we're in.
        """
        
        # Ensure that we are not already at the last stage.
        if self.stage == 3:
            raise ValueError(
                    "'advance_stage()' cannot be called on a stage 3 transaction."
        )
        
        # Offers. Ensure that both the buyer and seller have accepted the resource.
        if self.stage == 0 and \
           (self.buyer_accepted_offer != self.seller_accepted_offer) or \
           (self.buyer_accepted_offer == None):
                raise ValueError("the buyer and seller offers are not equal.")

        # Contracts. Ensure that contracts are equal, & both parties have accepted.
        elif self.stage == 1:
            if not self.buyer_accepted_contract or not self.seller_accepted_contract:
                raise ValueError("buyer and seller must both accept contract.")
            if not self.contracts_equal:
                raise ValueError("contracts must be equal.")

            # Create the closing stage.
            self.create_closing()

        # Closing. Check the closing conditions are satisfied.
        elif self.stage == 2:
            raise ValueError("this has yet to be implemented.")

        self.stage += 1
        self.save()

    def get_offers(self, user_id):
        """
        Returns a queryset for the given user's offers.
        Args:
            user_id: The ID of the given user.
        """

        return self.offers.filter(owner=user_id).order_by("-timestamp")
    
    def create_closing(self):
        """
        Create a Closing object for this transaction according to the type
        of property we're operating on.
        """
        
        closing_type = self.kproperty._type
        closing = AbstractClosingFactory.create_closing(
                    closing_type=closing_type, transaction=self)

        return closing

    def check_diff(self):
        """
        Update the `contracts_equal` field according to the latest state
        of both contracts. Note, this can only be called when both contracts
        belonging to the transaction are in existence.
        """

        assert self.contracts.all().count() == 2, (
                "error: `check_diff()` can only be called when the transaction "
                "in question has both contracts in existence."
        )

        contracts = self.contracts.all().prefetch_related("dynamic_clauses")
        _c0 = { clause.title: clause.actual_type.value
                for clause in contracts[0].dynamic_clauses.all()
        }
        _c1 = { clause.title: clause.actual_type.value
                for clause in contracts[1].dynamic_clauses.all()
        }

        self.contracts_equal = _c0 == _c1
        self.save()

    def delete(self, *args, **kwargs):
        """
        Overrides the default signal handling on related models.
        """

        # Handle signals. If we're in the offer stage then we want to create an
        # offer notification. If we're in the contract stage then we do not.
        if self.stage == 0:
            self._dampen = True; self.save()
        else:
            self._dampen = True; self._fired = True; self.save()

        super(Transaction, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

