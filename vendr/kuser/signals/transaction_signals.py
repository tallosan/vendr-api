#
# Transaction signals.
#
# ===============================================================

from django.dispatch import receiver

from transaction.signals.dispatch import offer_withdraw_signal
from kuser.models import OfferNotification


@receiver(offer_withdraw_signal)
def offer_withdraw_receiver(sender, **kwargs):

    # Create offer notification, and publish it.
    offer = sender
    notification = OfferNotification.objects.create_deletion_notification(offer)
    notification.publish()

