#
# Notification models.
#
# ==========================================================================

from __future__ import unicode_literals

import uuid

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_delete
from django.conf import settings
from django.dispatch import receiver

from transaction.models import Transaction, Offer, Contract


''' [Static] Handler for creating notifications. We determine the type of
    notification (creation or deletion) first, then route the signal instance
    off to the appropriate Notification class.
    N.b. -- The actual creating is deferred to the routed class's create_() method.
    Args:
        sender: The class responsible for sending the signal.
        instance: The instance of the class that was saved.
'''
@staticmethod
@receiver(signal=[post_save, post_delete], sender=Transaction)
@receiver(signal=[post_save, post_delete], sender=Offer)
@receiver(signal=[post_save, post_delete], sender=Contract)
def handler(sender, instance, **kwargs):

    # Creation notification. Note, we need to ensure that the sender was just created.
    if (kwargs['signal'] == post_save) and (kwargs['created']):
        notification_type = resolve_type(instance.__class__)
        notification_type.objects.create_creation_notification(instance)

    # Deletion notification.
    elif kwargs['signal'] == post_delete:
        notification_type = resolve_type(instance.__class__)
        notification_type.objects.create_deletion_notification(instance)
    

''' Determine the notification type for the given sender.
    Args:
        instance_class: The model that sent the notification.
'''
def resolve_type(sender_class):

    class_mappings = {
                        Transaction: TransactionNotification,
                        Offer: OfferNotification,
                        Contract: ContractNotification
    }

    return class_mappings[sender_class]


'''   Base notification manager. '''
class BaseNotificationManager(models.Manager):

    ''' [Abstract] Notification for instance creation. Children must implement this. '''
    def create_creation_notification(self):
        raise NotImplementedError('error: all notifications must implement this.')

    ''' [Abstract] Notification for instance deletion. Children must implement this. '''
    def create_deletion_notification(self):
        raise NotImplementedError('error: all notifications must implement this.')


'''   Responsible for creating all types of transaction notifications.'''
class TransactionNotificationManager(BaseNotificationManager):

    ''' Notification on Transaction creation. '''
    def create_creation_notification(self, instance):
        return

    ''' Notification on Transaction deletion.
        Args:
            instance: The Transaction that was just deleted.
    '''
    def create_deletion_notification(self, instance):
        
        curr_user = instance._current_user
        recipient = instance.buyer if (curr_user == instance.seller) \
                                      else instance.seller
        sender = curr_user.profile.first_name
        description = sender + ' has ended his transaction with you on property ' + \
                      str(instance.kproperty) + '.'

        notification = self.create(recipient=recipient, sender=sender,
                                   description=description,
                                   transaction=instance,
        )

        return notification


'''   Responsible for creating all types of offer notifications.'''
class OfferNotificationManager(BaseNotificationManager):
 
    ''' Notification on Offer creation.
        Args:
            instance: The Offer that was just created.
    '''
    def create_creation_notification(self, instance):
        
        transaction = instance.transaction
        
        # Deterimine the notification's recipient, and format its description.
        recipient   = transaction.buyer if (instance.owner == transaction.seller) \
                                      else transaction.seller
        sender      = instance.owner.profile.first_name
        description = sender + ' has sent you a new offer on your property ' + \
                      str(transaction.kproperty) + '.'
        
        # Create the notification.
        notification = self.create(recipient=recipient, sender=sender,
                                   description=description,
                                   transaction=transaction,
                                   offer=instance
        )
        
        return notification
       
    ''' Notification on Offer deletion.
        Args:
            instance: The Offer that was just deleted.
    '''
    def create_deletion_notification(self, instance):
        
        # TODO: Prevent this from firing on Transaction delete.
        transaction = instance.transaction
        recipient   = transaction.buyer if (instance.owner == transaction.seller) \
                                        else transaction.seller
        sender      = instance.owner.profile.first_name
        description = sender + ' has withdrawn their offer on your property ' + \
                      str(transaction.kproperty) + '.'

        notification = self.create(recipient=recipient, sender=sender,
                                   description=description,
                                   transaction=transaction,
                                   offer=instance
        )

        return notification


'''   Contract notification manager. '''
class ContractNotificationManager(models.Manager):

    ''' [Abstract] Notification for instance creation. Children must implement this. '''
    def create_creation_notification(self):
        raise NotImplementedError('error: all notifications must implement this.')

    ''' [Abstract] Notification for instance deletion. Children must implement this. '''
    def create_deletion_notification(self):
        raise NotImplementedError('error: all notifications must implement this.')


'''   [Abstract] Base notification model. '''
class BaseNotification(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Note, we do not need to have a hard reference to the sender.
    recipient   = models.ForeignKey(settings.AUTH_USER_MODEL,
                    related_name='notifications', on_delete=models.CASCADE)
    sender      = models.CharField(max_length=100)
    
    description = models.CharField(max_length=150, blank=True)
    is_viewed   = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    
    ''' Custom string representation. '''
    def __str__(self):
        
        return self.description


'''   A notification on a transaction. '''
class TransactionNotification(BaseNotification):

    transaction = models.ForeignKey(Transaction, related_name='notifications',
                    on_delete=models.SET_NULL, null=True)
    objects = TransactionNotificationManager()
    

'''   A notification on a transaction's offers. '''
class OfferNotification(TransactionNotification):

    offer = models.ForeignKey(Offer, related_name='notifications',
                on_delete=models.SET_NULL, null=True)
    objects = OfferNotificationManager()


'''   A notification on a transaction's contracts. '''
class ContractNotification(TransactionNotification):
 
    contract = models.ForeignKey(Contract, related_name='notifications',
                on_delete=models.SET_NULL, null=True)
    objects  = ContractNotificationManager()

