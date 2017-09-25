#
# Scheduling for open houses.
#
# ================================================================

from __future__ import unicode_literals
from django.db import models
from django.conf import settings

import uuid


"""   Container for RSVP models. """
class OpenHouse(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
            editable=False, db_index=True)
    
    kproperty = models.ForeignKey('Property', related_name='open_houses',
                    on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner',
                on_delete=models.CASCADE)
    
    # The start & end of the open house.
    start = models.DateTimeField()
    end   = models.DateTimeField()


"""   Represents a user's RSVP to an open house. """
class RSVP(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
            editable=False, db_index=True)
    open_house = models.ForeignKey('OpenHouse', related_name='rsvp_list',
                    on_delete=models.CASCADE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                related_name='rsvp_schedule', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['open_house', 'owner']

