#
# Periodic tasks for Property objects and related models.
#
# ================================================================

from __future__ import absolute_import
from celery import shared_task

from kproperty.models import Property, OpenHouse, RSVP


""" Unfeature a property after a day. """
@shared_task
def property_unfeature_task():
    
    for kproperty in Property.objects.unfeature_queue():
        kproperty.is_featured = False
        kproperty.save()


""" Perform a soft-delete on open house models after they have
    been completed. """
@shared_task
def openhouse_clear_task():

    #TODO: Pending design.
    pass

