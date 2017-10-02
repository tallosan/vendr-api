#
# Scheduling for open houses.
#
# ================================================================

from __future__ import unicode_literals
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone

import uuid

class OpenHouseManager(models.Manager):

    """ Queue of Open Houses that are starting 'soon', where we define
        soon to mean 'in x hours'. """
    def starting_soon_queue(self):

        # Determine which open houses start in the next `notify_before`
        # window (defaults to 1 hour before).
        notify_before = timedelta(hours=1)
        notify_window = timezone.now() + notify_before
        starting_soon_queue = super(OpenHouseManager, self).get_queryset().\
                filter(start__gte=timezone.now()).\
                filter(start__lte=notify_window)

        return starting_soon_queue

    """ Queue of inactive Open Houses. We define 'inactive' to mean
        any open house that has already taken place. """
    def inactive_queue(self):

        inactive_queue = super(OpenHouseManager, self).get_queryset().\
                filter(_is_active=True).\
                filter(end__lte=timezone.now())

        return inactive_queue


"""   Container for RSVP models. """
class OpenHouse(models.Model):

    objects = OpenHouseManager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
            editable=False, db_index=True)
    
    kproperty = models.ForeignKey('Property', related_name='open_houses',
                    on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner',
                on_delete=models.CASCADE)
    
    # The start & end of the open house.
    start = models.DateTimeField()
    end   = models.DateTimeField()

    # Determines if the open house has taken place yet.
    _is_active = models.BooleanField(default=True)

    # Used to prevent duplicate notifications.
    _recipients_notified = models.BooleanField(default=False)


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

