#
# Scheduling App for open houses.
#
# ================================================================

from __future__ import unicode_literals
from django.db import models
from django.conf import settings

import uuid


'''   Container for RSVP models. '''
class OpenHouse(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
            editable=False, db_index=True)
    
    kproperty = models.ForeignKey('Property', related_name='open_house',
                    on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner',
                on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender',
                on_delete=models.CASCADE)
    
    # The start & end of the open house.
    start = models.DateTimeField()
    end   = models.DateTimeField()


'''   Represents a user's RSVP to an open house. '''
class RSVP(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
            editable=False, db_index=True)
    open_house = models.ForeignKey('OpenHouse', related_name='open_house',
                    on_delete=models.CASCADE)
    
    # N.B. -- We're removing reverse lookups, as it doesn't really make
    # sense for the user to be able to do that.
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+',
                on_delete=models.CASCADE)

