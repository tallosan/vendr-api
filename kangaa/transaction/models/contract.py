#
# Contract models and managers.
#
# ===========================================================================

from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from model_utils.managers import InheritanceManager

import uuid
import datetime
from collections import OrderedDict

from kproperty.models import Property
from .transaction import Transaction

from .text.static_clauses import STATIC_CLAUSES, CONDO_STATIC_CLAUSES, \
        COOP_STATIC_CLAUSES, COOWNERSHIP_STATIC_CLAUSES, MOBILE_STATIC_CLAUSES
from .text.dynamic_clauses import DYNAMIC_STANDARD_CLAUSES


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
        
        elif contract_type == 'house':
            contract_factory = HouseContract.objects
        
        elif contract_type == 'townhouse':
            contract_factory = TownhouseContract.objects

        elif contract_type == 'manufactured':
            contract_factory = ManufacturedContract.objects

        elif contract_type == 'vacant_land':
            contract_factory = VacantLandContract.objects

        # Create the contract.
        contract = contract_factory.create_contract(owner=owner,
                    transaction=transaction, **kwargs)
        return contract

# Contract Managers
# ===========================================================================

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
        deposit_clause = DepositClause.objects.create(contract=contract, value=2)
        completion_date = CompletionDateClause.objects.create(contract=contract)
        irrevocability_clause = IrrevocabilityClause.objects.create(contract=contract)
        payment_clause = PaymentMethodClause.objects.create(contract=contract,
                value='Credit Card')
        buyer_arranges_mortgage = BuyerArrangesMortgageClause.objects.\
                create(contract=contract)

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
            
                # Generic clauses.
                STATIC_CLAUSES['title_search'],
                STATIC_CLAUSES['inspection_omit'],
                STATIC_CLAUSES['property_tax_assessment'],
                STATIC_CLAUSES['alt_alterations'],
                STATIC_CLAUSES['occupancy_agreement'],
                STATIC_CLAUSES['alt_documents_request'],

                # Co-Op specific clauses.
                COOP_STATIC_CLAUSES['corporation_documentation'],
                COOP_STATIC_CLAUSES['meetings'],
                COOP_STATIC_CLAUSES['title'],
                COOP_STATIC_CLAUSES['loan_discharge'],
                COOP_STATIC_CLAUSES['adjustments']

        ]

    def create_contract(self, owner, transaction, **kwargs):

        contract = super(CoOpContractManager, self).\
                     create_contract(owner, transaction, **kwargs)

        # Dynamic Clauses:
        chattels_inc = ChattelsIncludedClause.objects.create(contract=contract)
        fixtures_exc = FixturesExcludedClause.objects.create(contract=contract)
        rented_items = RentalItemsClause.objects.create(contract=contract)
        equipment = EquipmentClause.objects.create(contract=contract)
        environment = EnvironmentClause.objects.create(contract=contract)
        maintenance = MaintenanceClause.objects.create(contract=contract)
        chattels_and_fixs = ChattelsAndFixsClause.objects.create(contract=contract)
        
        return contract


class CondoContractManager(CoOpContractManager):
    
    ''' Initialize this manager with any necessary additional static clauses. '''
    def __init__(self):
        
        super(CondoContractManager, self).__init__()
        self.static_clauses += [

            # Generic clauses.
            STATIC_CLAUSES['title'],
            STATIC_CLAUSES['status_certificate_and_mgmt'],
            STATIC_CLAUSES['meetings'],
            STATIC_CLAUSES['condo_laws_acknowledgement_pre'],
            STATIC_CLAUSES['unit_insurance'],
            STATIC_CLAUSES['alt_document_prep'],
            STATIC_CLAUSES['alt_residency'],

            # Condo specific clauses.
            CONDO_STATIC_CLAUSES['approval_of_agreement'],
            CONDO_STATIC_CLAUSES['alterations'],
            CONDO_STATIC_CLAUSES['documents_request'],
            CONDO_STATIC_CLAUSES['discharge'],
            CONDO_STATIC_CLAUSES['adjustments']
        ]
                
    ''' Create a Condo Contract.
        Args:
            owner: The owner of the contract.
            transaction: The transaction this contract belongs to.
    '''
    def create_contract(self, owner, transaction, **kwargs):

        contract = super(CondoContractManager, self).\
                     create_contract(owner, transaction, **kwargs)

        # Dynamic Clauses:
        mortgage_deadline = MortgageDeadlineClause.objects.create(contract=contract)
        uffi = UFFIClause.objects.create(contract=contract)
        
        return contract

class CoOwnershipContractManager(BaseContractManager):

    ''' Initialize this manager with any necessary additional static clauses. '''
    def __init__(self):
        
        super(CoOwnershipContractManager, self).__init__()
        self.static_clauses += [
                
                # Generic clauses.
                STATIC_CLAUSES['title'],
                STATIC_CLAUSES['title_search'],
                STATIC_CLAUSES['inspection_omit'],
                STATIC_CLAUSES['property_tax_assessment'],
                STATIC_CLAUSES['alt_alterations'],
                STATIC_CLAUSES['occupancy_agreement'],
                STATIC_CLAUSES['alt_documents_request'],

                # Co-Ownership specific clauses.
                COOWNERSHIP_STATIC_CLAUSES['residency'],
                COOWNERSHIP_STATIC_CLAUSES['adjustments']
        ]
 
    ''' Create a CoOwnership Contract.
        Args:
            owner: The owner of the contract.
            transaction: The transaction this contract belongs to.
    '''
    def create_contract(self, owner, transaction, **kwargs):
        
        contract = super(CoOwnershipContractManager, self).\
                     create_contract(owner, transaction, **kwargs)

        # Dynamic Clauses:
        chattels_inc = ChattelsIncludedClause.objects.create(contract=contract)
        fixtures_exc = FixturesExcludedClause.objects.create(contract=contract)
        rented_items = RentalItemsClause.objects.create(contract=contract)
        mortgage_deadline = MortgageDeadlineClause.objects.create(contract=contract)
        equipment = EquipmentClause.objects.create(contract=contract)
        environment = EnvironmentClause.objects.create(contract=contract)
        maintenance = MaintenanceClause.objects.create(contract=contract)
        chattels_and_fixs = ChattelsAndFixsClause.objects.create(contract=contract)
 
        return contract



class HouseContractManager(BaseContractManager):
 
    ''' Initialize this manager with any necessary additional static clauses. '''
    def __init__(self):
        
        super(HouseContractManager, self).__init__()
        self.static_clauses += [
                
                # Generic clauses.
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
    
    ''' Create a House Contract.
        Args:
            owner: The owner of the contract.
            transaction: The transaction this contract belongs to.
    '''
    def create_contract(self, owner, transaction, **kwargs):
        
        contract = super(HouseContractManager, self).\
                     create_contract(owner, transaction, **kwargs)

        # Dynamic Clauses:
        chattels_inc = ChattelsIncludedClause.objects.create(contract=contract)
        fixtures_exc = FixturesExcludedClause.objects.create(contract=contract)
        rented_items = RentalItemsClause.objects.create(contract=contract)
        mortgage_deadline = MortgageDeadlineClause.objects.create(contract=contract)
        equipment = EquipmentClause.objects.create(contract=contract)
        environment = EnvironmentClause.objects.create(contract=contract)
        survey = SurveyDeadlineClause.objects.create(contract=contract)
        maintenance = MaintenanceClause.objects.create(contract=contract)
        uffi = UFFIClause.objects.create(contract=contract)
        chattels_and_fixs = ChattelsAndFixsClause.objects.create(contract=contract)
 
        return contract


class TownhouseContractManager(HouseContractManager):

    def __init__(self):

        super(TownhouseContractManager, self).__init__()
        self.static_clauses += [
            
            # Generic clauses.
            STATIC_CLAUSES['status_certificate_and_mgmt'],
            STATIC_CLAUSES['meetings'],
            STATIC_CLAUSES['condo_laws_acknowledgement_pre'],
        ]
    
    ''' Create a Townhouse House Contract.
        Args:
            owner: The owner of the contract.
            transaction: The transaction this contract belongs to.
    '''
    def create_contract(self, owner, transaction, **kwargs):
        
        contract =  super(TownhouseContractManager, self).\
              create_contract(owner, transaction, **kwargs)

        # Dynamic Clauses:
 
        return contract


class ManufacturedContractManager(BaseContractManager):
    
    ''' Initialize this manager with any necessary additional static clauses. '''
    def __init__(self):
        
        super(ManufacturedContractManager, self).__init__()
        self.static_clauses += [

                # Generic clauses.
                STATIC_CLAUSES['residency'],
                STATIC_CLAUSES['non_residency'],
                STATIC_CLAUSES['adjustments'],
                STATIC_CLAUSES['tender'],

                # Manufactured specific clauses.
                MOBILE_STATIC_CLAUSES['rules_and_regs'],
                MOBILE_STATIC_CLAUSES['lease'],
                MOBILE_STATIC_CLAUSES['title'],
                MOBILE_STATIC_CLAUSES['documents_request'],
                MOBILE_STATIC_CLAUSES['discharge'],
                MOBILE_STATIC_CLAUSES['inspection'],
                MOBILE_STATIC_CLAUSES['insurance']
        ]
    
    ''' Create a Manufactured Contract.
        Args:
            owner: The owner of the contract.
            transaction: The transaction this contract belongs to.
    '''
    def create_contract(self, owner, transaction, **kwargs):
        
        contract = super(ManufacturedContractManager, self).\
              create_contract(owner, transaction, **kwargs)

        # Dynamic Clauses:
        chattels_inc = ChattelsIncludedClause.objects.create(contract=contract)
        fixtures_exc = FixturesExcludedClause.objects.create(contract=contract)
        rented_items = RentalItemsClause.objects.create(contract=contract)
        mortgage_deadline = MortgageDeadlineClause.objects.create(contract=contract)
        equipment = EquipmentClause.objects.create(contract=contract)
        environment = EnvironmentClause.objects.create(contract=contract)
        maintenance = MaintenanceClause.objects.create(contract=contract)
        chattels_and_fixs = ChattelsAndFixsClause.objects.create(contract=contract)
 
        return contract


'''   Vacant land contract manager.'''
class VacantLandContractManager(BaseContractManager):
    
    ''' Initialize this manager with any necessary additional static clauses. '''
    def __init__(self):
        
        super(VacantLandContractManager, self).__init__()
        self.static_clauses += [
                
                # Generic clauses.
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
        
        contract = super(VacantLandContractManager, self).\
                     create_contract(owner, transaction, **kwargs)

        mortgage_deadline = MortgageDeadlineClause.objects.create(contract=contract)
        survey = SurveyDeadlineClause.objects.create(contract=contract)

        return contract


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
    
    @property
    def clauses(self):
        
        clauses = []
        clauses += self.static_clauses.all()
        clauses += [
                        d_clause.actual_type
                        for d_clause in self.dynamic_clauses.all()
        ]
        
        return clauses

    def save(self, *args, **kwargs):

        if self.transaction.contracts.filter(owner=self.owner).count() >= 1:
            raise ValueError('error: this user already has a contract.')

        super(Contract, self).save(*args, **kwargs)

class CoOpContract(Contract):
    objects = CoOpContractManager()

class CondoContract(Contract):
    objects = CondoContractManager()

class ManufacturedContract(Contract):
    objects = ManufacturedContractManager()

class HouseContract(Contract):
    objects = HouseContractManager()

class TownhouseContract(HouseContract):
    objects = TownhouseContractManager()

class VacantLandContract(Contract):
    objects = VacantLandContractManager

# ===========================================================================

class Clause(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # The Contract this clause belongs to.
    contract = models.ForeignKey(Contract, related_name='clauses',
                    on_delete=models.CASCADE)
    title     = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    @property
    def serializer(self):
        raise NotImplementedError('error: this property must exist for all clauses.')

# ==========================================================================

'''   Static Clauses are immutable and ubiquitous. '''
class StaticClause(Clause):
    
    contract = models.ForeignKey(Contract, related_name='static_clauses',
                    on_delete=models.CASCADE)

    preview   = models.TextField()
    is_active = models.BooleanField(default=True, editable=False)

    @property
    def serializer(self):
        
        return 'StaticClauseSerializer'

# ==========================================================================

'''   Dynamic Clauses are designed on a per-contract basis via user input. '''
class DynamicClause(Clause):

    prompt    = models.CharField(max_length=75, editable=False)
    preview   = models.TextField()
    contract  = models.ForeignKey(Contract, related_name='dynamic_clauses',
                    on_delete=models.CASCADE)

    # Clause category.
    CATEGORIES = (
            ('F', 'Financial'),
            ('D', 'Deadline'),
            ('U', 'Upkeep'),
            ('P', 'Possessions')
    )
    category   = models.CharField(choices=CATEGORIES, max_length=15)

    # How we display this clause on the front-end.
    UI_TYPES = (
            ('TEXT', 'text'),
            ('DATE', 'date'),
            ('DROPDOWN', 'dropdown'),
            ('CHIP', 'chip'),
            ('TOGGLE', 'toggle')
    )

    # Inheritance scheme.
    _content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    actual_type   = GenericForeignKey('_content_type', 'id')
    
    ''' We have to override this in order to create our inheritance scheme. '''
    def save(self, *args, **kwargs):

        if not self.pk:
            self.actual_type = self

        super(DynamicClause, self).save(*args, **kwargs)

    @property
    def preview(self):
        raise NotImplementedError('error: all children must implement this method.')
    
    @property
    def generator(self):

        generator = {
                        'category': self.category,
                        'prompt': self.prompt,
                        'value': self.value,
                        'ui_type': self.ui_type
        }

        return generator

    
    @property
    def serializer(self):
        return 'DynamicClauseSerializer'

class DynamicTextClause(DynamicClause):

    # 'value' is deffered to the child classes to set. HTTP doesn't care aobut
    # the data type (int, float, string, etc.) as they are all rende the same.
    ui_type = models.CharField(max_length=10, default='TEXT', editable=False)
    
    class Meta: abstract = True

class DynamicToggleClause(DynamicClause):

    value   = models.BooleanField(default=True)
    ui_type = models.CharField(max_length=6, default='TOGGLE', editable=False)

    class Meta: abstract = True

class DynamicDropdownClause(DynamicClause):
     
    # 'value' is deffered to the child classes to set. HTTP doesn't care aobut
    # the data type (int, float, string, etc.) as they are all rende the same.
    options = ArrayField(models.CharField(max_length=15))
    ui_type = models.CharField(max_length=10, default='DROPDOWN', editable=False)

    class Meta: abstract = True

    @property
    def generator(self):

        generator = super(DynamicDropdownClause, self).generator
        generator['options'] = self.options

        return generator

    @property
    def serializer(self):
        return 'DropdownClauseSerializer'

class DynamicChipClause(DynamicClause):
 
    value = ArrayField(models.CharField(max_length=15), default=list)
    ui_type = models.CharField(max_length=10, default='CHIP', editable=False)
    
    class Meta: abstract = True

class DynamicDateClause(DynamicClause):

    value = models.DateField(auto_now_add=True)
    ui_type = models.CharField(max_length=10, default='DATE', editable=False)
    
    class Meta: abstract = True

# ==========================================================================

class CompletionDateClause(DynamicDateClause):

    def save(self, *args, **kwargs):

        if not self.pk:
            self.category = 'D'
            self.title = 'Completion Date'
            self.prompt = 'Sale Completion Date'

        super(CompletionDateClause, self).save(*args, **kwargs)

    @property
    def preview(self):

        day = self.value.day
        month = self.value.month
        year = self.value.year

        preview = DYNAMIC_STANDARD_CLAUSES['completion_date'].\
                  format(day, month, year)
        return preview

class IrrevocabilityClause(DynamicDateClause):

    def save(self, *args, **kwargs):

        if not self.pk:
            self.category = 'D'
            self.title = 'Irrevocability'
            self.prompt = 'Cancellation Deadline'

        super(IrrevocabilityClause, self).save(*args, **kwargs)

    @property
    def preview(self):

        deadline_month = self.value.month
        deadline_day   = self.value.day
        preview = DYNAMIC_STANDARD_CLAUSES['irrevocability']. \
                  format(deadline_month, deadline_day)
        
        return preview

class MortgageDeadlineClause(DynamicDateClause):

    def save(self, *args, **kwargs):

        if not self.pk:
            self.category = 'D'
            self.title = 'Mortgage Date'
            self.prompt = 'Mortgage Deadline'

        super(MortgageDeadlineClause, self).save(*args, **kwargs)

    @property
    def preview(self):

        preview = DYNAMIC_STANDARD_CLAUSES['mortgage_date'].\
                  format(self.value)
        return preview

class SurveyDeadlineClause(DynamicDateClause):

    def save(self, *args, **kwargs):
        
        if not self.pk:
            self.category = 'P'
            self.title = 'Survey'
            self.prompt = 'Request a Land Survey'

        super(SurveyDeadlineClause, self).save(*args, **kwargs)

    @property
    def preview(self):

        year = self.value.year
        month = self.value.month
        day = self.value.day

        date = ('{}/{}/{}').format(year, month, day)

        preview = DYNAMIC_STANDARD_CLAUSES['survey_date'].\
                  format(date)

        return preview

class DepositClause(DynamicTextClause):

    value = models.PositiveIntegerField(null=True)

    def save(self, *args, **kwargs):

        if not self.pk:
            self.title = 'Deposit'
            self.category = 'D'
            self.prompt = 'Deposit Deadline'

        super(DepositClause, self).save(*args, **kwargs)
    
    @property
    def preview(self):

        transaction = self.contract.transaction

        # Fields: Deposit amount, Seller name, Deposit Deadline.
        #deposit = transaction.seller_accepted_offer.deposit
        #seller_name = transaction.seller.full_name
        deposit = 3000
        seller_name = 'macmasterrace101'
        deposit_deadline = self.value

        preview = DYNAMIC_STANDARD_CLAUSES['deposit'].\
                  format(deposit, seller_name, deposit_deadline)

        return preview

class ChattelsAndFixsClause(DynamicToggleClause):

    def save(self, *args, **kwargs):

        if not self.pk:
            self.title = 'Chattels and Fixtures'
            self.category = 'U'
            self.prompt = 'Ensure Chattels & Fixtures are in good working order'

        super(ChattelsAndFixsClause, self).save(*args, **kwargs)

    @property
    def preview(self):

        preview = DYNAMIC_STANDARD_CLAUSES['chattels_and_fixs']
        return preview

class BuyerArrangesMortgageClause(DynamicToggleClause):

    def save(self, *args, **kwargs):

        if not self.pk:
            self.title = 'Buyer Arranging Mortgage'
            self.category = 'F'
            self.prompt = 'Buyer Arranges Mortgage'

        super(BuyerArrangesMortgageClause, self).save(*args, **kwargs)

    @property
    def preview(self):

        preview = DYNAMIC_STANDARD_CLAUSES['buyer_mrtg_arrange']
        return preview

class EquipmentClause(DynamicToggleClause):

    def save(self, *args, **kwargs):

        if not self.pk:
            self.title = 'Equipment'
            self.category = 'U'
            self.prompt = 'Equipment State'

        super(EquipmentClause, self).save(*args, **kwargs)

    @property
    def preview(self):

        preview = DYNAMIC_STANDARD_CLAUSES['equipment']
        return preview

class EnvironmentClause(DynamicToggleClause):

    def save(self, *args, **kwargs):

        if not self.pk:
            self.title = 'Environment'
            self.category = 'U'
            self.prompt = 'Environmental Clause'

        super(EnvironmentClause, self).save(*args, **kwargs)

    @property
    def preview(self):

        preview = DYNAMIC_STANDARD_CLAUSES['environmental']
        return preview

class MaintenanceClause(DynamicToggleClause):

    def save(self, *args, **kwargs):

        if not self.pk:
            self.title = 'Maintenance'
            self.category = 'U'
            self.prompt = 'Seller will provide maintenance on the property prior ' \
                          'to purchase'
        super(MaintenanceClause, self).save(*args, **kwargs)

    @property
    def preview(self):

        preview = DYNAMIC_STANDARD_CLAUSES['maintenance']
        return preview

class UFFIClause(DynamicToggleClause):

    def save(self, *args, **kwargs):

        if not self.pk:
            self.title = 'UFFI and Vermiculite'
            self.category = 'U'
            self.prompt = 'Void UFFI & Vermiculite Warning'

        super(UFFIClause, self).save(*args, **kwargs)

    @property
    def preview(self):

        preview = DYNAMIC_STANDARD_CLAUSES['uffi']
        return preview

class PaymentMethodClause(DynamicDropdownClause):

    value = models.CharField(max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):

        if not self.pk:
            self.category = 'F'
            self.title = 'Payment Method'
            self.prompt = 'Payment Method'
            self.options = ['Credit Card', 'Cheque', 'Cash']
        
        super(PaymentMethodClause, self).save(*args, **kwargs)
    
    @property
    def preview(self):

        payment_method = self.value
        preview = 'The Buyer agrees to pay the Seller on completion of this ' + \
                  'transaction via a ' + payment_method + ' payment.'
        return preview

class ChattelsIncludedClause(DynamicChipClause):

    def save(self, *args, **kwargs):

        if not self.pk:
            self.category = 'P'
            self.title = 'Chattels Included'
            self.prompt = 'Chattels Included'
        
        super(ChattelsIncludedClause, self).save(*args, **kwargs)

    @property
    def preview(self):
        
        chattels = ', '.join(self.value)
        preview = DYNAMIC_STANDARD_CLAUSES['chattels_inc'].\
                  format(chattels)

        return preview

class FixturesExcludedClause(DynamicChipClause):

    def save(self, *args, **kwargs):

        if not self.pk:
            self.category = 'P'
            self.title = 'Fixtures Excluded'
            self.prompt = 'Fixtures Excluded'

        super(FixturesExcludedClause, self).save(*args, **kwargs)

    @property
    def preview(self):

        fixtures = ', '.join(self.value)
        preview = DYNAMIC_STANDARD_CLAUSES['fixtures_exc'].\
                  format(fixtures)

        return preview

class RentalItemsClause(DynamicChipClause):

    def save(self, *args, **kwargs):

        if not self.pk:
            self.category = 'P'
            self.title = 'Rental Items'
            self.prompt = 'Rented Items on Property'

        super(RentalItemsClause, self).save(*args, **kwargs)

    @property
    def preview(self):

        rented_items = ', '.join(self.value)
        preview = DYNAMIC_STANDARD_CLAUSES['rented_items'].\
                  format(rented_items)
                  
        return preview

