from __future__ import unicode_literals

import uuid

from django.db import models
from django.conf import settings

from .transaction import Transaction


'''   Model representing an offer on a property, or a counter-offer. '''
class Offer(models.Model):

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4,
                    editable=False)

    # The user who made the offer, and the transaction the offer belongs to.
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='offers',
                    on_delete = models.CASCADE, db_index=True)
    transaction = models.ForeignKey(Transaction, related_name='offers',
                    on_delete=models.CASCADE)
    
    offer       = models.FloatField()
    deposit     = models.FloatField()
    comment     = models.CharField(max_length=350, blank=True)

    timestamp   = models.DateTimeField(auto_now_add=True)

