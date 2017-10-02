#
# Periodic tasks for Property objects and related models.
#
# ================================================================

from __future__ import absolute_import
from celery import shared_task

import django.dispatch

from kproperty.models import Property, OpenHouse, RSVP
from kproperty.signals.dispatch import openhouse_start_signal


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

    for open_house in OpenHouse.objects.inactive_queue():
        open_house._is_active = False
        open_house.save()


""" Send the user a notification if an open house is starting soon. """
@shared_task
def openhouse_start():
    
    # Notify anyone who has RSVP'd to an open house that is starting soon.
    for openhouse in OpenHouse.objects.starting_soon_queue():
        if not openhouse._recipients_notified:
            openhouse_start_signal.send(sender=openhouse)

