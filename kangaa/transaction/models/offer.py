from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from .transaction import Transaction


'''   Model representing an offer on a property, or a counter-offer. '''
class Offer(models.Model):

    user        = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='offers',
                    on_delete = models.CASCADE, db_index=True)
    
    # The transaction that this offer belongs to.
    transaction = models.OneToOneField(Transaction, related_name='offer',
                    on_delete=models.CASCADE)
    
    offer       = models.FloatField()
    deposit     = models.FloatField()
    comment     = models.CharField(max_length=350, blank=True)

    timestamp   = models.DateTimeField(auto_now_add=True)

