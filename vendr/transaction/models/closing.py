#
# Closing models and managers.
#
# ===========================================================================

from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


#TODO: 
# Use Smart Contracts for escrow (Ethereum looks most promising for this).
#


class Closing(models.Model):
    
    transaction = models.ForeignKey(Transaction, related_name='closing')


class Document(models.Model):

    closing = models.ForeignKey(Closing, related_name='documents')
    description = models.TextField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        pass


class Requirement(models.Model):

    closing = models.ForeignKey(Closing, related_name='requirements')
    clause = models.OneToOneField(DynamicClause, related_name='requirement')
    
    # The state of the requirement.
    accepted        = models.BooleanField(default=False)
    buyer_accepted  = models.BooleanField(default=False)
    seller_accepted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        # Set the requirement state according to the buyer & seller's stance.
        if self.buyer_accepted is True and self.seller_accepted is True:
            self.accepted = True

        super(Requirement, self).save(*args, **kwargs)

