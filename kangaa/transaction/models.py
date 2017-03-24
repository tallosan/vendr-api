from __future__ import unicode_literals

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
    def create(self, buyer, seller, kproperty, **extra_fields):
        
        # Ensure that the buyer, seller, and property are specified.
        if any(arg is None for arg in {buyer, seller, kproperty}):
            raise ValueError('error: buyer, seller, or kproperty not specified.')
        
        # Create the transaction.
        now = timezone.now()
        transaction = self.model(buyer=buyer, seller=seller, kproperty=kproperty,
                                 start_date=now
        )
        transaction.save(using=self._db)

        # Create the contract.
        contract = Contract.objects.create(transaction=transaction, kproperty=kproperty)

        return transaction


'''   Transaction model. Each Transaction has a buyer, a seller, and a property, along 
      with a set of Offers and a Contract. Each Transaction has 3 stages. '''
class Transaction(models.Model):

    # The buyer, seller, and the property this transaction is on.
    buyer       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='buyer_trans')
    seller      = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='seller_trans')
    kproperty   = models.ForeignKey(Property, related_name='property')

    # Stage 1: Offer Stage.
    b_offer     = models.IntegerField()
    s_offer     = models.IntegerField()

    offer       = models.IntegerField()

    # Stage 2: Negotiation Stage.
    b_contract  = models.FileField(blank=True)
    s_contract  = models.FileField(blank=True)

    contract    = models.FileField(blank=True)

    # Stage 3: Closing Stage.
    closing     = models.IntegerField(blank=True)

    # The transaction stage we're in.
    STAGES      = (
                    (0, 'OFFER_STAGE'),
                    (1, 'NEGOTIATION_STAGE'),
                    (2, 'CLOSING_STAGE')
    )
    
    stage       = models.IntegerField(choices=STAGES, default=0)
    mutex       = models.IntegerField()

    # Meta:
    start_date  = models.DateTimeField(auto_now_add=True)
    objects     = TransactionManager()

    ''' Custom save method. The key here is how the mutex is handled. '''
    def save(self, *args, **kwargs):
        print self.id

    ''' Move the transaction stage up, assuming we aren't already in the final stage. '''
    def next_stage(self):

        # Final stage.
        if self.stage == 2:
            raise Http404('error: transaction is at final stage already.')

        self.stage += 1

    ''' String representation for Transaction models. '''
    def __str__(self):

        return  'buyer ' + str(self.buyer) + \
                ' and seller ' + str(self.seller) + \
                ' on property ' + str(self.kproperty)


'''   Custom Contract Manager. '''
class ContractManager(models.Manager):

    ''' Create a contract model. '''
    def _create(self, transaction, kproperty):
        
        contract = self.model(transaction=transaction, kproperty=kproperty)
        contract.save(using=self._db)

        return contract

    ''' Creates a standard model. '''
    def create_standard(self, transaction, kproperty):
        
        # Create clauses.
        return self._create(transaction, kproperty)


'''   [Abstract] Contract model. Each Contract is attached to a single Transaction,
      and is made up of Clauses. '''
class Contract(models.Model):

    # The Transaction that this contract belongs to.
    transaction = models.OneToOneField(Transaction, related_name='contract',
                    on_delete=models.CASCADE)
    objects     = InheritanceManager()
    
    #TODO: Start filtering the common clauses accross models.

'''   Standard contract for CoOp properties. '''
class CoOpContract(Contract):
    pass


'''   Standard contract for Condo properties. '''
class CondoContract(Contract):
    pass


'''   Standard contract for Mobile properties. '''
class MobileContract(Contract):
    pass


'''   Standard contract for Freehold properties. '''
class FreeholdContract(Contract):
    pass


'''   Standard contract for POTL Freehold properties. '''
class POTLFreeholdContract(FreeholdContract):
    pass


'''   Clause model. '''
class Clause(models.Model):

    # The Contract this clause belongs to.
    contract    = models.ForeignKey(Contract, related_name='clauses')
    
    # The clause body, an explanation of what it means, and the value
    # that the user fills in.
    #TODO: Implement Singleton on each generic clause body.
    body        = models.CharField(max_length=250)
    explanation = models.CharField(max_length=250)
    value       = models.CharField(max_length=50, blank=True)

