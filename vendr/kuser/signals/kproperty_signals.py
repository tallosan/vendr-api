#
# KProperty signals.
#
# ===============================================================

from django.dispatch import receiver

from kproperty.signals.dispatch import openhouse_create_signal, \
        openhouse_start_signal, openhouse_change_signal, openhouse_cancel_signal
from kuser.models import OpenHouseCreateNotification, OpenHouseChangeNotification, \
        OpenHouseCancelNotification, OpenHouseStartNotification


""" Notify anyone who has favourited this property that the owner has
    created an open house on it. """
@receiver(openhouse_create_signal)
def openhouse_create_receiver(sender, **kwargs):

    openhouse = sender
    resource = kwargs['resource']
    for subscriber in openhouse.kproperty._subscribers.all():

        # Create the change notification.
        notification = OpenHouseCreateNotification.objects.create(
                recipient=subscriber,
                openhouse_owner=openhouse.owner.profile.first_name,
                openhouse_address=openhouse.kproperty.location.address,
                resource=resource
        )

        # Publish notification.
        notification.publish()


""" Notify anyone who has RSVP'd to an Open House of any changes. """
@receiver(openhouse_change_signal)
def openhouse_change_receiver(sender, **kwargs):

    openhouse = sender
    resource = kwargs['resource']
    for rsvp in openhouse.rsvp_list.all():

        # Create the change notification.
        recipient = rsvp.owner
        notification = OpenHouseChangeNotification.objects.create(
                recipient=recipient,
                openhouse_owner=openhouse.owner.profile.first_name,
                openhouse_address=openhouse.kproperty.location.address,
                resource=resource
        )

        # Publish notification.
        notification.publish()


""" Notify anyone who has RSVP'd to an Open House of any changes. """
@receiver(openhouse_cancel_signal)
def openhouse_cancel_receiver(sender, **kwargs):

    openhouse = sender
    resource = kwargs['resource']
    for rsvp in openhouse.rsvp_list.all():

        # Create the change notification.
        recipient = rsvp.owner
        notification = OpenHouseCancelNotification.objects.create(
                recipient=recipient,
                openhouse_owner=openhouse.owner.profile.first_name,
                openhouse_address=openhouse.kproperty.location.address,
                resource=resource
        )

        # Publish notification.
        notification.publish()


""" Notify anyone who has RSVP'd to an Open House 1 hour before it starts. """
@receiver(openhouse_start_signal)
def openhouse_start_receiver(sender, **kwargs):

    # Send a notification to each user that has RSVP'd.
    openhouse = sender
    resource = kwargs['resource']
    for rsvp in openhouse.rsvp_list.all():

        # Create notification.
        recipient = rsvp.owner; sender = None
        notification = OpenHouseStartNotification.objects.create(
                recipient=recipient,
                openhouse_owner=openhouse.owner.profile.first_name,
                openhouse_address=openhouse.kproperty.location.address,
                resource=resource
        )

        # Publish notification.
        notification.publish()

    # Set the open house flag to prevent duplicate notifications.
    openhouse._recipients_notified = True; openhouse.save()

