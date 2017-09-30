#
# Transaction signals.
#
# ===============================================================

from django.dispatch import receiver

from transaction.signals.dispatch import transaction_withdraw_signal, \
        offer_withdraw_signal, contract_withdraw_signal
from kuser.models import TransactionNotification, \
        OfferNotification, ContractNotification, \
        TransactionWithdrawNotification


@receiver(transaction_withdraw_signal)
def transaction_withdraw_receiver(sender, **kwargs):

    transaction = sender; request_sender = kwargs['request_sender']

    # Determine the recipient's role in the transaction.
    recipient, is_owner = (transaction.buyer, False) \
        if (request_sender == transaction.seller) \
        else (transaction.seller, True)

    # Create the transaction notification, and publish it.
    notification = TransactionWithdrawNotification.objects.create(
            sender=request_sender.profile.first_name,
            recipient=recipient,
            kproperty_address=transaction.kproperty.location.address,
            _is_owner=is_owner)
    notification.publish()


@receiver(offer_withdraw_signal)
def offer_withdraw_receiver(sender, **kwargs):

    # Create offer notification, and publish it.
    offer = sender
    notification = OfferNotification.objects.\
            create_deletion_notification(offer)
    notification.publish()


@receiver(contract_withdraw_signal)
def contract_withdraw_receiver(sender, **kwargs):

    # Create contract notification, and publish it.
    contract = sender
    notification = ContractNotification.objects.\
            create_deletion_notification(contract)
    notification.publish()

