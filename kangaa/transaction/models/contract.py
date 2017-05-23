#
# Contract models and managers.
#
# ===========================================================================

from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.conf import settings

from model_utils.managers import InheritanceManager

import uuid
import datetime
from collections import OrderedDict

from kproperty.models import Property
from .transaction import Transaction

from .text.clauses import STATIC_CLAUSES


class AbstractContractFactory(object):

    ''' Create a contract of the given type.
        Args:
            contract_type: The type of contract to create.
            transaction: The transaction that this contract will belong to.
            **kwargs: Any additional arguments to create the contract with.
    '''
    @staticmethod
    def create_contract(contract_type, owner, transaction, **kwargs):
        
        # Get the factory responsible for creating our contract type.
        contract_factory = None
        if contract_type == 'coop':
            contract_factory = CoOpContract.objects
        
        elif contract_type == 'coownership':
            contract_factory = CoOwnershipContract.objects
        
        elif contract_type == 'condo':
            contract_factory = CondoContract.objects
        
        elif contract_type == 'freehold':
            contract_factory = FreeholdContract.objects

        # Create the contract.
        contract = contract_factory.create_contract(owner=owner,
                    transaction=transaction, **kwargs)
        return contract

#
# Contract Managers
# ===========================================================================
#

'''   [Abstract] '''
class BaseContractManager(models.Manager):

    def __init__(self):
        
        self.static_clauses = [
            STATIC_CLAUSES['completion_date_adjustments'], STATIC_CLAUSES['notices'],
            STATIC_CLAUSES['buyer_negligence'], STATIC_CLAUSES['electronic'],
            STATIC_CLAUSES['sales_tax'], STATIC_CLAUSES['deadline_extensions'],
            STATIC_CLAUSES['family_law_act'], STATIC_CLAUSES['personal_information'],
            STATIC_CLAUSES['agreement_in_writing'], STATIC_CLAUSES['time_and_date'],
        ]

        super(BaseContractManager, self).__init__()

    ''' Create a contract model. '''
    def create_contract(self, owner, transaction, **kwargs):
        
        # Create a contract, and add static clauses to it.
        contract = self.create(owner=owner, transaction=transaction)
        self.add_static_clauses(contract)

        # Create clauses.
        #overview = OverviewClause.objects.create(contract=contract, date=date,
                    #buyer_name=buyer_name, seller_name=seller_name,
                    #address=address, sqr_ftg=sqr_ftg)
        #deposit = DepositClause.objects.create()
        return contract


    ''' (Helper) Adds the appropriate static clauses to the given contract. '''
    def add_static_clauses(self, contract):

        # Create static clauses.
        for static_clause in self.static_clauses:
            clause = StaticClause.objects.create(contract=contract,
                        title=static_clause['title'],
                        preview=static_clause['preview']
            )


class CoOpContractManager(BaseContractManager):

    ''' Initialize this manager with any necessary additional static clauses. '''
    def __init__(self):

        super(CoOpContractManager, self).__init__()
        self.static_clauses += [
                STATIC_CLAUSES['title_search'],
                STATIC_CLAUSES['inspection_omit'],
                STATIC_CLAUSES['property_tax_assessment'],
        ]

    def create_contract(self, owner, transaction, **kwargs):

        return super(CoOpContractManager, self).\
                     create_contract(owner, transaction, **kwargs)


class CondoContractManager(CoOpContractManager):
    
    ''' Initialize this manager with any necessary additional static clauses. '''
    def __init__(self):
        
        super(CondoContractManager, self).__init__()
        self.static_clauses += [
            STATIC_CLAUSES['title'],
            STATIC_CLAUSES['title_search'],
            STATIC_CLAUSES['inspection_omit'],
            STATIC_CLAUSES['property_tax_assessment'],
        ]

    ''' Create a Condo Contract.
        Args:
            owner: The owner of the contract.
            transaction: The transaction this contract belongs to.
    '''
    def create_contract(self, owner, transaction, **kwargs):

        return super(CondoContractManager, self).\
                     create_contract(owner, transaction, **kwargs)


class CoOwnershipContractManager(BaseContractManager):

    ''' Initialize this manager with any necessary additional static clauses. '''
    def __init__(self):
        
        super(CoOwnershipContractManager, self).__init__()
        self.static_clauses += [
                STATIC_CLAUSES['title'],
                STATIC_CLAUSES['title_search'],
                STATIC_CLAUSES['inspection_omit'],
                STATIC_CLAUSES['property_tax_assessment'],
        ]
 
    ''' Create a CoOwnership Contract.
        Args:
            owner: The owner of the contract.
            transaction: The transaction this contract belongs to.
    '''
    def create_contract(self, owner, transaction, **kwargs):
        
        return super(CoOwnershipContractManager, self).\
                     create_contract(owner, transaction, **kwargs)


class FreeholdContractManager(BaseContractManager):
 
    ''' Initialize this manager with any necessary additional static clauses. '''
    def __init__(self):
        
        super(FreeholdContractManager, self).__init__()
        self.static_clauses += [
                STATIC_CLAUSES['title'],
                STATIC_CLAUSES['title_search'],
                STATIC_CLAUSES['documents_request'],
                STATIC_CLAUSES['discharge'],
                STATIC_CLAUSES['inspection_omit'],
                STATIC_CLAUSES['insurance'],
                STATIC_CLAUSES['planning'],
                STATIC_CLAUSES['document_prep'],
                STATIC_CLAUSES['residency'],
                STATIC_CLAUSES['non_residency'],
                STATIC_CLAUSES['adjustments'],
                STATIC_CLAUSES['property_tax_assessment'],
                STATIC_CLAUSES['tender'],
        ]
    
    ''' Create a Freehold Contract.
        Args:
            owner: The owner of the contract.
            transaction: The transaction this contract belongs to.
    '''
    def create_contract(self, owner, transaction, **kwargs):
        
        return super(FreeholdContractManager, self).\
                     create_contract(owner, transaction, **kwargs)


class POTLFreeholdContractManager(FreeholdContractManager):

    #static_clauses += []
    
    ''' Create a POTL Freehold Contract.
        Args:
            owner: The owner of the contract.
            transaction: The transaction this contract belongs to.
    '''
    def create_contract(self, transaction, **kwargs):
        
        super(POTLFreeholdContractManager, self).\
              create_contract(owner, transaction, **kwargs)


class MobileContractManager(BaseContractManager):
    
    ''' Initialize this manager with any necessary additional static clauses. '''
    def __init__(self):
        
        super(MobileContractManager, self).__init__()
        self.static_clauses += [
                STATIC_CLAUSES['residency'],
                STATIC_CLAUSES['non_residency'],
                STATIC_CLAUSES['adjustments'],
                STATIC_CLAUSES['tender'],
        ]
    
    ''' Create a Mobile Contract.
        Args:
            owner: The owner of the contract.
            transaction: The transaction this contract belongs to.
    '''
    def create_contract(self, owner, transaction, **kwargs):
        
        super(MobileContractManager, self).\
              create_contract(owner, transaction, **kwargs)


'''   Vacant land contract manager.'''
class VacantLandContractManager(BaseContractManager):
    
    ''' Initialize this manager with any necessary additional static clauses. '''
    def __init__(self):
        
        super(VacantLandContractManager, self).__init__()
        self.static_clauses += [
                STATIC_CLAUSES['title'],
                STATIC_CLAUSES['title_search'],
                STATIC_CLAUSES['documents_request'],
                STATIC_CLAUSES['discharge'],
                STATIC_CLAUSES['insurance'],
                STATIC_CLAUSES['planning'],
                STATIC_CLAUSES['document_prep'],
                STATIC_CLAUSES['residency'],
                STATIC_CLAUSES['non_residency'],
                STATIC_CLAUSES['adjustments'],
                STATIC_CLAUSES['property_tax_assessment'],
                STATIC_CLAUSES['tender'],
        ]
    
    ''' Create a Vacantland Contract.
        Args:
            owner: The owner of the contract.
            transaction: The transaction this contract belongs to.
    '''
    def create_contract(self, owner, transaction, **kwargs):
        
        return super(VacantLandContractManager, self).\
                     create_contract(owner, transaction, **kwargs)


# ===========================================================================

'''   [Abstract] Contract model. Each Contract is attached to a single Transaction,
      and is made up of Clauses. '''
class Contract(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # The Transaction that this contract belongs to.
    transaction = models.ForeignKey(Transaction, related_name='contracts',
                    on_delete=models.CASCADE)
    timestamp   = models.DateTimeField(auto_now_add=True)
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contracts',
                    on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['transaction', 'owner']
    # 'generator': [
    #         {'prompt': 'Date of Signing', 'values': [], 'type': 'string', 'order': 1},
    #         {'prompt': 'Method of Payment', 'values': [], 'type': 'string', 'order': 0},
    # ]

'''   Standard contract for CoOp properties. '''
class CoOpContract(Contract):
    
    objects = CoOpContractManager()


'''   Standard contract for Condo properties. '''
class CondoContract(Contract):

    objects = CondoContractManager()


'''   Standard contract for Mobile properties. '''
class MobileContract(Contract):

    objects = MobileContractManager()


'''   Standard contract for Freehold properties. '''
class FreeholdContract(Contract):

    objects = FreeholdContractManager()


'''   Standard contract for POTL Freehold properties. '''
class POTLFreeholdContract(FreeholdContract):
    
    objects = POTLFreeholdContractManager()


# ===========================================================================


'''   Clause model. '''
class Clause(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # The Contract this clause belongs to.
    contract = models.ForeignKey(Contract, related_name='clauses',
                    on_delete=models.CASCADE)
    title     = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


'''   Static Clauses are immutable and ubiquitous. '''
class StaticClause(Clause):
    
    contract = models.ForeignKey(Contract, related_name='static_clauses',
                    on_delete=models.CASCADE)

    preview   = models.TextField()
    is_active = models.BooleanField(default=True, editable=False)


'''   Dynamic Clauses are designed on a per-contract basis via user input. '''
class DynamicClause(Clause):
 
    contract = models.ForeignKey(Contract, related_name='dynamic_clauses',
                    on_delete=models.CASCADE)

    generator = JSONField(default=list([]))
    preview   = models.TextField()

    class Meta:
        abstract = True

    @property
    def preview(self):
        raise NotImplementedError('error: all children must implement this method.')
    
    @property
    def generator(self):
        raise NotImplementedError('error: all children must implement this method.')


class DropdownClause(Clause):
 
    contract = models.ForeignKey(Contract, related_name='dropdown_clauses',
                    on_delete=models.CASCADE)
    options = ArrayField(models.CharField(max_length=15))

