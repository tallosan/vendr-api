from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from model_utils.managers import InheritanceManager

from kproperty.models import Property
from .transaction import Transaction


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
    
    timestamp   = models.DateTimeField(auto_now_add=True)
    objects     = InheritanceManager()
    #TODO: Start filtering the common clauses accross models.
    
    ''' Determine if the contract has been changed since the session started. '''
    def has_changed(self):

        # Hash.
        return False


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
    #key         = models.C
    #body        = models.CharField(max_length=250)
    explanation = models.CharField(max_length=250)
    value       = models.CharField(max_length=50, blank=True)

