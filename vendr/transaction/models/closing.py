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

from . import Transaction, Clause
   

class AbstractClosingFactory(object):

    ''' Create a closing of the given type.
        Args:
            closing_type -- The type of closing to create.
            transaction -- The transaction that this closing will belong to.
            **kwargs: Any additional arguments to create the closing with.
    '''
    def create_closing(self, closing_type, transaction):

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

	# Create the closing.
	closing = closing_factory.create_closing(transaction=transaction,
			**kwargs)
	return closing

# ===========================================================================

'''   [Abstract] '''
class BaseClosingManager(models.Manager):
    
    def create_closing(self, transaction, **kwargs):
        pass

class CoOpClosingManager(BaseClosingManager):
    pass

class CondoClosingManager(BaseClosingManager):
    pass

class HouseClosingManager(BaseClosingManager):
    pass

class TownhouseClosingManager(BaseClosingManager):
    pass

class ManufacturedClosingManager(BaseClosingManager):
    pass

class VacantLandClosingManager(BaseClosingManager):
    pass

# ===========================================================================

'''   [Abstract] '''
class Closing(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
            editable=False, db_index=True)

    transaction = models.ForeignKey(Transaction, related_name='closing')
 
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

    title = models.CharField(max_length=25)
    description = models.TextField()
    
    ''' Raises a NotImplementedError. Note, we are not making this class
        abstract, as we'd like to use the multiple-inheritance heirarchy. That
        being said, we do want this class to behave like it's abstract -- i.e.
        we never want to actually create an instance of Document(). '''
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

    clause_type = models.ForeignKey(ContentType, null=True)
    clause_id = models.UUIDField(null=True)
    clause = GenericForeignKey('clause_type', 'clause_id')

    # Clauses must be approved by both parties in order for them to be
    # added to the document. We'll use this flag to determine a clause's state.
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('clause_type', 'clause_id')

    def save(self, *args, **kwargs):
        
        # Ensure that the linked Clause is, indeed, a Clause object.
        if not issubclass(self.clause_type.model_class(), Clause):
            raise AttributeError(
                    'error: clause must be either an instance of StaticClause '
                    'or DynamicClause. instead, clause is of type {}'.
                    format(self.clause_type.model_class().__class__)
            )

        super(DocumentClause, self).save(*args, **kwargs)


'''   Some Documents have a set of clauses attached to them -- e.g. the
      Ammendments document contains a set of clauses that have been ammended.
      This mixin supports any necessary functionality that a document will need
      to manage its clauses. '''
class ClauseDocumentMixin(object):
    
    model = DocumentClause

    ''' Add a clause to the document.
        Args:
            clause -- The clause to be added (can be either static or dynamic).
    '''
    def add_clause(self, clause, accepted=False):

        new_clause = self.model.objects.create(document=self.document,
                        clause=clause, accepted=accepted)
                
    ''' The approved clauses that have been approved on the document. '''
    @property
    def approved_clauses(self):
        return self.document_clauses.filter(accepted=True)

    ''' The pending clauses that have yet to be approved. '''
    @property
    def pending_clauses(self):
        return self.document_clauses.filter(accepted=False)

            
'''   The Ammendments document is where any accepted clause changes
      and/or additions go. '''
class Ammendments(Document, ClauseDocumentMixin):
    
    closing = models.OneToOneField(Closing, related_name='ammendments',
                on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):

        if self._state.adding:
            self.title = 'Ammendments'
            self.description = ''

        super(Document, self).save(*args, **kwargs)


'''   The Waiver document is where any accepted clause removals go. '''
class Waiver(Document, ClauseDocumentMixin):
    
    closing = models.OneToOneField(Closing, related_name='waiver',
                on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        if self._state.adding:
            self.title = 'Waiver'
            self.description = ''

        super(Document, self).save(*args, **kwargs)


'''   The Notice of Fullfillment document manages the state of the contract
      requirements. E.g. has the deposit been sent with the correct amount? '''
class NoticeOfFulfillment(Document):
    
    closing = models.OneToOneField(Closing, related_name='notice_of_fulfillment',
                on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        if self._state.adding:
            self.title = 'Notice Of Fulfillment'
            self.description = 'hi'

        super(Document, self).save(*args, **kwargs)


'''   The Mutual Release document handles the mutual termination of
      a transaction. '''
class MutualRelease(Document):
    
    closing = models.OneToOneField(Closing, related_name='mutual_release',
                on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        if self._state.adding:
            self.title = 'Mutual Release'
            self.description = 'hi'

        super(Document, self).save(*args, **kwargs)
