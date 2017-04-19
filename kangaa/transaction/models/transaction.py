from __future__ import unicode_literals

import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone

from model_utils.managers import InheritanceManager

from kproperty.models import Property
#from transaction.exceptions import FieldPermissionError


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
    buyer       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='buyer',
                    editable=False, on_delete=models.CASCADE)
    seller      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seller',
                    editable=False, on_delete=models.CASCADE)
    kproperty   = models.ForeignKey(Property, related_name='kproperty',
                    editable=False, on_delete=models.CASCADE)

    # Stage 1: Offer Stage.
    # [Foreign Key: buyer_offer, seller_offer, offer]

    # Stage 2: Negotiation Stage.
    # [Foreign Key: buyer_contract, seller_contract, contract]
    
    # Stage 3: Closing Stage.

    # The transaction stage we're in.
    STAGES      = (
                    (0, 'OFFER_STAGE'),
                    (1, 'NEGOTIATION_STAGE'),
                    (2, 'CLOSING_STAGE')
    )
    stage       = models.IntegerField(choices=STAGES, default=0)
    start_date  = models.DateTimeField(auto_now_add=True)
    
    objects     = TransactionManager()

    ''' Returns True if the user has permission to access the given fields,
        and False if not.
        Args:
            user_id: The ID of the User.
            fields: The fields the User is attempting to modify.
    '''
    def check_field_permissions(self, user_id, fields):
        
        print fields
        # The mapping between the user types, and the fields they can access.
        protected_fields = {
                                self.buyer.id: [ self.buyer_offer, self.buyer_contract ],
                                self.seller: [
                                                self.seller_offer, self.offer,
                                                self.seller_contract, self.contract
                                ]
        }
     
        # Determine whether or not the user is valid.
        if user_id not in protected_fields.keys():
            raise ValueError('error: user is not involved in this transaction.')
    
        # Return False if a field is not in the user's permission scope.
        for field in protected_fields[user_id]:
            print field

        #return True
        return False

    ''' Move to the next stage in the transaction. N.B. -- Only the seller has
        permission to move from the Offer stage to the Contract stage.
    '''
    def next_stage(self):

        pass

    def get_offers(self, user_id):

        return self.offers.filter(owner=user_id)


    ''' String representation for Transaction models. '''
    def __str__(self):

        return 'buyer: ' + str(self.buyer) + ', seller: ' + str(self.seller) + ', ' + \
               'property: ' + str(self.kproperty)
