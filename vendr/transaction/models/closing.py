#
# Closing models and managers.
#
# ===========================================================================

from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from .contract import Clause
from .text.closing import DOCUMENTS_TEXT
   

class AbstractClosingFactory(object):

    ''' Create a closing of the given type.
        Args:
            closing_type -- The type of closing to create.
            transaction -- The transaction that this closing will belong to.
            **kwargs: Any additional arguments to create the closing with.
    '''
    @staticmethod
    def create_closing(closing_type, transaction, **kwargs):

        # Get the factory responsible for creating our closing type.
        closing_factory = None
        if closing_type == 'coop':
            closing_factory = CoOpClosing.objects
        
        elif closing_type == 'condo':
            closing_factory = CondoClosing.objects
        
        elif closing_type == 'house':
            closing_factory = HouseClosing.objects
        
        elif closing_type == 'townhouse':
            closing_factory = TownhouseClosing.objects

        elif closing_type == 'manufactured':
            closing_factory = ManufacturedClosing.objects

        elif closing_type == 'vacant_land':
            closing_factory = VacantLandClosing.objects
        else:
            raise ValueError('error: invalid closing type.')

	# Create the closing.
	closing = closing_factory.create_closing(transaction=transaction,
			**kwargs)
	return closing

# ===========================================================================

'''   [Abstract] '''
class BaseClosingManager(models.Manager):
    
    def create_closing(self, transaction, **kwargs):

        # Create closing model.
        _property_descriptor = self.format_descriptor(transaction)
        closing = self.create(transaction=transaction,
                    _property_descriptor=_property_descriptor,
                    _document_header=DOCUMENTS_TEXT['header'],
                    _document_footer=DOCUMENTS_TEXT['footer']
        )

        # Create the four Closing documents.
        amendment = Amendments.objects.create(closing=closing)
        waiver = Waiver.objects.create(closing=closing)
        notice_of_fulfillment = NoticeOfFulfillment.objects.create(closing=closing)
        mutual_release = MutualRelease.objects.create(closing=closing)

        return closing

    def format_descriptor(self, transaction):
        raise NotImplementedError('error: all children must implement this.')


class CoOpClosingManager(BaseClosingManager):
    
    ''' Formats a CoOp transaction's closing document's property descriptor.
        Args:
            transaction (Transaction) -- The transaction this Closing exists on.
    '''
    def format_descriptor(self, transaction):

        descriptor = DOCUMENTS_TEXT['coop_descriptor'].format(
                        transaction.kproperty.unit_num,
                        transaction.kproperty.location.address,
                        transaction.kproperty.corporation_name
        )

        return descriptor


class CondoClosingManager(BaseClosingManager):

    ''' Formats a Condo transaction's closing document's property descriptor.
        Args:
            transaction (Transaction) -- The transaction this Closing exists on.
    '''
    def format_descriptor(self, transaction):

        descriptor = DOCUMENTS_TEXT['condo_descriptor'].format(
                        transaction.kproperty.location.address,
                        transaction.kproperty.unit_num
        )

        return descriptor


class HouseClosingManager(BaseClosingManager):

    ''' Formats a House transaction's closing document's property descriptor.
        Args:
            transaction (Transaction) -- The transaction this Closing exists on.
    '''
    def format_descriptor(self, transaction):

        descriptor = DOCUMENTS_TEXT['house_descriptor'].format(
                        transaction.kproperty.location.address,
                        transaction.kproperty.sqr_ftg
        )

        return descriptor


class TownhouseClosingManager(BaseClosingManager):

    ''' Formats a Townhouse transaction's closing document's property descriptor.
        Args:
            transaction (Transaction) -- The transaction this Closing exists on.
    '''
    def format_descriptor(self, transaction):

        descriptor = DOCUMENTS_TEXT['townhouse_descriptor'].format(
                        transaction.kproperty.location.address,
                        transaction.kproperty.unit_num
        )

        return descriptor


class ManufacturedClosingManager(BaseClosingManager):

    ''' Formats a Manufactured transaction's closing document's property descriptor.
        Args:
            transaction (Transaction) -- The transaction this Closing exists on.
    '''
    def format_descriptor(self, transaction):

        descriptor = DOCUMENTS_TEXT['manufactured_descriptor'].format(
                        transaction.kproperty.manufacturer,
                        transaction.kproperty.serial_num,
                        transaction.kproperty.year,
                        transaction.kproperty.length, transaction.kproperty.width,
                        transaction.kproperty.location.address,
                        transactoin.kproperty.mobile_park
        )

        return descriptor


class VacantLandClosingManager(BaseClosingManager):

    ''' Formats a Vacant Land transaction's closing document's property descriptor.
        Args:
            transaction (Transaction) -- The transaction this Closing exists on.
    '''
    def format_descriptor(self, transaction):

        descriptor = DOCUMENTS_TEXT['vacantland_descriptor'].format(
                        transaction.kproperty.location.address,
                        transaction.kproperty.sqr_ftg
        )

        return descriptor

# ===========================================================================

'''   [Abstract] '''
class Closing(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
            editable=False, db_index=True)

    transaction = models.OneToOneField('Transaction', related_name='closing',
                    on_delete=models.CASCADE)

    # These are fields that pertain to each document associated with the
    # closing stage. As such, it makes sense to store them in one place, as opposed
    # to four (in each doc).
    _property_descriptor = models.TextField(blank=False)
    _document_header = models.TextField(blank=False)
    _document_footer = models.TextField(blank=False)


class CoOpClosing(Closing):
    objects = CoOpClosingManager()


class CondoClosing(Closing):
    objects = CondoClosingManager()


class HouseClosing(Closing):
    objects = HouseClosingManager()


class TownhouseClosing(Closing):
    objects = HouseClosingManager()


class ManufacturedClosing(Closing):
    objects = ManufacturedClosingManager()


class VacantLandClosing(Closing):
    objects = VacantLandClosingManager()

# ===========================================================================

'''   [Abstract] '''
class Document(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
            editable=False, db_index=True)

    title = models.CharField(max_length=43)
    content = models.TextField(blank=False)
    explanation = models.TextField()
    signing_date = models.DateField(blank=True, null=True)
    
    ''' Raises a NotImplementedError. Note, we are not making this class
        abstract, as we'd like to use the multiple-inheritance heirarchy. That
        being said, we do want this class to behave like it's abstract -- we
        never want to actually create an instance of Document(). '''
    def save(self, *args, **kwargs):
        raise NotImplementedError(
                'error: cannot instantiate a Document. try creating one'
                'of its children.'
        )


'''   A clause that is part of a document. '''
class DocumentClause(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
            editable=False, db_index=True)

    document = models.ForeignKey(Document, related_name='document_clauses',
                on_delete=models.CASCADE)

    # Generic foreign key to allow us to reference both static & dynamic clauses.
    clause_type = models.ForeignKey(ContentType, null=True)
    clause_id = models.UUIDField(null=True)
    clause = GenericForeignKey('clause_type', 'clause_id')

    # Clauses must be approved by both parties in order for them to be added
    # to the document. Thus, we'll use this flag to determine a clause's state.
    accepted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        
        # Ensure that the linked Clause is, indeed, a Clause object.
        if not issubclass(self.clause_type.model_class(), Clause):
            raise AttributeError(
                    'error: clause must be either an instance of `StaticClause` '
                    'or `DynamicClause`. instead, clause is of type {}'.
                    format(self.clause_type.model_class().__class__)
            )

        super(DocumentClause, self).save(*args, **kwargs)

    def __str__(self):
        return self.clause.title


'''   Some Documents have a set of clauses attached to them -- e.g. the
      Amendments document contains a set of clauses that have been ammended.
      This mixin supports any necessary functionality that a document will need
      to manage its clauses. '''
class ClauseDocumentMixin(object):
    
    clause_model = DocumentClause

    ''' Add a clause to the document. As clause objects do not have the
        necessary functionality to be useful in a document, this method
        is essentially a wrapper for whichever model we choose to use
        to give them these necessary functionalities -- in this case,
        the DocumentClause model.
        Args:
            clause -- The clause (static or dynamic) to be added.
    '''
    def add_clause(self, clause, accepted=False):

        new_clause = self.clause_model.objects.create(document=self, clause=clause,
                        accepted=accepted)

    ''' The approved clauses that have been approved on the document. '''
    @property
    def approved_clauses(self):
        return self.document_clauses.filter(accepted=True)

    ''' The pending clauses that have yet to be approved. '''
    @property
    def pending_clauses(self):
        return self.document_clauses.filter(accepted=False)

    ''' Raise NotImplementedError. Updates a document's content by iterating
        through its clauses and checking for any new additions to the
        `approved` set. This should be called after each clause addition.
    '''
    def reformat_content(self):
        raise NotImplementedError(
                'error: `reformat_content()` must implemented by each Document '
                        'using this mixin.'
        )

            
'''   The Amendments document is where any accepted clause changes
      and/or additions go. '''
class Amendments(Document, ClauseDocumentMixin):
    
    closing = models.OneToOneField(Closing, related_name='amendments',
                on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):

        if self._state.adding:
            self.title = 'Amendment to Agreement of Purchase and Sale'
            self.content = DOCUMENTS_TEXT['amendment']
        
        super(Document, self).save(*args, **kwargs)

    ''' Updates an Amendment document's content by iterating through its
        clauses and checking for any new additions to the `approved` set. '''
    def reformat_content(self):

        contract = self.closing.transaction.contracts.all()[0]
        contract_signing_date = None
        amended_clauses = ', '.join([str(clause) for clause in self.approved_clauses])
        irrevocability_date = contract.dynamic_clauses.get(title='Irrevocability').\
                actual_type.value
        self.content = self.content.format(contract_signing_date,
                amended_clauses, irrevocability_date)

        self.save()


'''   The Waiver document is where any accepted clause removals go. '''
class Waiver(Document, ClauseDocumentMixin):
    
    closing = models.OneToOneField(Closing, related_name='waiver',
                on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        if self._state.adding:
            self.title = 'Waiver'
            self.content = DOCUMENTS_TEXT['waiver']

        super(Document, self).save(*args, **kwargs)

    ''' Updates a Waiver document's content by iterating through its clauses and
        checking for any new additions to the `approved` set. '''
    def reformat_content(self):

        contract = self.closing.transaction.contracts.all()[0]
        contract_signing_date = None
        waiver_clauses = ', '.join([str(clause) for clause in self.approved_clauses])
        self.content = self.content.format(contract_signing_date,
                amended_clauses, self.signing_date)

        self.save()


'''   The Notice of Fullfillment document manages the state of the contract
      requirements. E.g. has the deposit been sent with the correct amount? '''
class NoticeOfFulfillment(Document, ClauseDocumentMixin):
    
    closing = models.OneToOneField(Closing, related_name='notice_of_fulfillment',
                on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        # N.B. -- We need to save the Document first before we can add the
        # pending clauses.
        if self._state.adding:
            self.title = 'Notice Of Fulfillment'
            self.content = DOCUMENTS_TEXT['notice_of_fulfillment']
            super(Document, self).save(*args, **kwargs)
            self._add_pending_clauses()
        else:
            super(Document, self).save(*args, **kwargs)

    ''' Adds a set clauses that require fulfillment to the document's
        pending queue. '''
    def _add_pending_clauses(self):
        
        # Add each required clause to our pending queue. N.B. -- We're
        # explicitly setting `accepted` here for no reason other than brevity.
        contract = self.closing.transaction.contracts.all()[0]
        for clause in contract.required_clauses:
            self.add_clause(clause, accepted=False)

        self.reformat_content()

    ''' Updates a Notice of Fulfillments document's content by iterating through
        its clauses and checking for any new additions to the `approved` set. '''
    def reformat_content(self):

        contract = self.closing.transaction.contracts.all()[0]
        contract_signing_date = None
        clauses = ', '.join([str(clause) for clause in self.pending_clauses])
        self.content = self.content.format(
                contract_signing_date, clauses)

        self.save()


'''   The Mutual Release document handles the mutual termination of
      a transaction. '''
class MutualRelease(Document):
    
    closing = models.OneToOneField(Closing, related_name='mutual_release',
                on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        if self._state.adding:
            self.title = 'Mutual Release'
            self.content = DOCUMENTS_TEXT['mutual_release']

        super(Document, self).save(*args, **kwargs)

