#
# KProperty signals.
#
# ===============================================================

from django.dispatch import receiver

from kproperty.signals.dispatch import openhouse_start_signal
from kuser.models import OpenHouseStartNotification


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

