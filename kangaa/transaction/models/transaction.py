from __future__ import unicode_literals

import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone

from model_utils.managers import InheritanceManager

from kproperty.models import Property


'''   Custom Transaction Manager. '''
class TransactionManager(models.Manager):
    
    ''' Creates a Transaction model, along with the given Contract.
        Args:
            buyer: The User who wants to buy the property. 
            seller: The User who is selling the property.
            kproperty: The Property in question.
    '''
    def create_transaction(self, buyer, seller, kproperty, **extra_fields):
        
        # Ensure that the buyer, seller, and property are specified.
        if any(arg is None for arg in {buyer, seller, kproperty}):
            raise ValueError('error: buyer, seller, or kproperty not specified.')
        
        # Ensure that the seller actually owns the property.
        if seller.id != kproperty.owner.id:
            raise ValueError('error: seller id does not match property owner id.')

        # Create the transaction.
        now = timezone.now()
        transaction = self.create(buyer=buyer, seller=seller, kproperty=kproperty,
                        start_date=now, **extra_fields
        )

        # Set buyer & seller permissions.
        #buyer.add_permission(...)
        return transaction


'''   Transaction model. Each Transaction has a buyer, a seller, and a property, along 
      with a set of Offers and a Contract. Each Transaction has 3 stages. '''
class Transaction(models.Model):

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4,
                        editable=False, db_index=True)
    
    # The buyer, seller, and the property this transaction is on.
    buyer     = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='buyer',
                    editable=False, on_delete=models.CASCADE)
    seller    = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seller',
                    editable=False, on_delete=models.CASCADE)
    kproperty = models.ForeignKey(Property, related_name='kproperty',
                    editable=False, on_delete=models.CASCADE)

    buyer_accepted_offer  = models.UUIDField(blank=True, null=True)
    seller_accepted_offer = models.UUIDField(blank=True, null=True)
    
    buyer_accepted_contract  = models.UUIDField(blank=True, null=True)
    seller_accepted_contract = models.UUIDField(blank=True, null=True)

    # The transaction stage we're in.
    STAGES     = (
                    (0, 'OFFER_STAGE'),
                    (1, 'NEGOTIATION_STAGE'),
                    (2, 'CLOSING_STAGE')
    )
    stage      = models.IntegerField(choices=STAGES, default=0)
    start_date = models.DateTimeField(auto_now_add=True)
    
    objects = TransactionManager()

    class Meta:
        unique_together = ['buyer', 'seller', 'kproperty']

    ''' Returns True if the user has permission to access the given fields,
        and False if not.
        Args:
            user_id: The ID of the User.
            fields: The fields the User is attempting to modify.
    '''
    def check_field_permissions(self, user_id, fields):

        # Mapping between users and the restricted fields that they cannot access.
        restricted_fields = {
                                self.buyer.pk: [ 'seller_accepted_offer',
                                                 'seller_accepted_contract',
                                ],
                                self.seller.pk: [ 'buyer_accepted_offer',
                                                  'buyer_accepted_contract'
                                ]
        }
        
        # Return False if a field is not in the user's permission scope.
        for field in fields:
            if field in restricted_fields[user_id]:
                return False

        return True

    ''' Advance to the next stage in the transaction. '''
    def advance_stage(self):
        
        # Ensure that we are not already at the last stage.
        if self.stage == 2:
            raise ValueError(
                    "error: 'advance_stage()' cannot be called on a stage 3 transaction."
        )

        # Determine the resource we are checking.
        if self.stage == 0:
            seller_resource = self.seller_accepted_offer
            buyer_resource  = self.buyer_accepted_offer
        elif self.stage == 1:
            seller_resource = self.seller_accepted_contract
            buyer_resource  = self.buyer_accepted_contract
        
        # Ensure that both the buyer and seller have accepted the resource.
        if (seller_resource is None) or (seller_resource != buyer_resource):
            raise ValueError("error: the buyer and seller resources are not equal.")

        # Increment the transaction stage.
        self.stage += 1

    ''' Returns a queryset for the given user's offers.
        Args:
            user_id: The ID of the given user.
    '''
    def get_offers(self, user_id):

        return self.offers.filter(owner=user_id).order_by('-timestamp')

    ''' String representation for Transaction models. '''
    def __str__(self):

        return str(self.pk)

