#
# Notification models.
#
# ==========================================================================

from __future__ import unicode_literals

import uuid

import redis

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_delete
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.dispatch import receiver

from transaction.models import Transaction, Offer, Contract


''' [Static] Handler for creating notifications. We determine the type of
    notification (creation or deletion) first, then route the signal instance
    off to the appropriate Notification class.
    N.b. -- The actual creating is deferred to the routed class's create_*() method.
    Args:
        sender: The class responsible for sending the signal.
        instance: The instance of the class that was saved.
'''
@staticmethod
@receiver(signal=[post_save, post_delete], sender=Offer)
@receiver(signal=[post_save, post_delete], sender=Contract)
def handler(sender, instance, **kwargs):

    # Creation notification. Note, we need to ensure that the sender was just created.
    if (kwargs['signal'] == post_save) and (kwargs['created']):
        notification_type = resolve_type(instance.__class__)
        notification = notification_type.objects.create_creation_notification(instance)

    # Deletion notification.
    elif kwargs['signal'] == post_delete:
        notification_type = resolve_type(instance.__class__)
        notification = notification_type.objects.create_deletion_notification(instance)
    
    # Publish to our Redis server iff a notification was created.
    if not notification: return
    channel = 'notifications.{}.{}'.format(notification.recipient.pk,
                notification.recipient.email)
    notification_json = notification.serialized
    
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    r.publish(channel, notification_json)
    

''' Determine the notification type for the given sender.
    Args:
        instance_class: The model that sent the notification.
'''
def resolve_type(sender_class):

    class_mappings = {
                        Offer: OfferNotification,
                        Contract: ContractNotification
    }

    return class_mappings[sender_class]


'''   Base notification manager. '''
class BaseNotificationManager(models.Manager):

    ''' [Abstract] Notification for instance creation. Children must implement this. '''
    def create_creation_notification(self, instance):
        raise NotImplementedError('error: all notifications must implement this.')

    ''' [Abstract] Notification for instance deletion. Children must implement this. '''
    def create_deletion_notification(self, instance):
        raise NotImplementedError('error: all notifications must implement this.')


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
                                   transaction=transaction.pk,
                                   offer=instance.pk
        )
        
        return notification
       
    ''' Notification on Offer deletion.
        Args:
            instance: The Offer that was just deleted.
    '''
    def create_deletion_notification(self, instance):
        
        # Determine if the transaction is dampening the signal. We dampen signals
        # because we only want to send one notification, however the cascading delete
        # on offers will make us send a notification for each offer on the transaction.
        transaction = instance.transaction
        if transaction._dampen and transaction._fired:
            return
        elif transaction._dampen and (not transaction._fired):
            transaction._fired = True; transaction.save()

        recipient   = transaction.buyer if (instance.owner == transaction.seller) \
                                        else transaction.seller
        sender      = instance.owner.profile.first_name
        description = sender + ' has withdrawn their offer on your property ' + \
                      str(transaction.kproperty) + '.'

        notification = self.create(recipient=recipient, sender=sender,
                                   description=description,
                                   transaction=transaction.pk,
                                   offer=instance.pk
        )
        print instance
        print instance.owner.profile
        print notification, notification.description

        return notification


'''   Contract notification manager. '''
class ContractNotificationManager(models.Manager):

    ''' Notification on Contract creation.
        Args:
            instance: The Contract that was just created.
    '''
    def create_creation_notification(self, instance):
        
        transaction = instance.transaction
        
        # Deterimine the notification's recipient, and format its description.
        recipient   = transaction.buyer if (instance.owner == transaction.seller) \
                                      else transaction.seller
        sender      = instance.owner.profile.first_name
        description = sender + ' has sent you a new contract for ' + \
                        str(transaction.kproperty) + '.'
        
        # Create the notification.
        notification = self.create(recipient=recipient, sender=sender,
                                   description=description,
                                   transaction=transaction.pk,
                                   contract=instance.pk
        )
        
        return notification
     
    ''' Notification on Transaction deletion.
        Args:
            instance: The Transaction that was just deleted.
    '''
    def create_deletion_notification(self, instance):
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

    # Meta data for child classes.
    _content_type = models.ForeignKey(ContentType, editable=False)
    actual_type  = GenericForeignKey('_content_type', 'id')

    class Meta:
        abstract = True

    ''' Custom save method. Sets actual type value. '''
    def save(self, *args, **kwargs):
        
        # Set the actual type if we're creating the model.
        if not self.pk:
            self.actual_type = self
        
        super(BaseNotification, self).save(*args, **kwargs)

    ''' Custom string representation. '''
    def __str__(self):
        
        return self.description

    ''' [Abstract] Returns the serializer type for this notification type. '''
    @staticmethod
    def get_serializer():
        raise NotImplementedError('error: all notifications must implement this.')


'''   A notification on a transaction. '''
class TransactionNotification(BaseNotification):

    transaction = models.UUIDField()
  

'''   A notification on a transaction's offers. '''
class OfferNotification(TransactionNotification):

    offer   = models.UUIDField()
    objects = OfferNotificationManager()

    ''' Returns the serializer for this notification type. '''
    @staticmethod
    def get_serializer():
        
        return 'OfferNotificationSerializer'

    ''' Return an offer notification serialized. '''
    @property
    def serialized(self):
        
        from kuser.serializers import OfferNotificationSerializer
        return OfferNotificationSerializer(self).data


'''   A notification on a transaction's contracts. '''
class ContractNotification(TransactionNotification):
 
    contract = models.UUIDField()
    objects  = ContractNotificationManager()
    
    ''' Returns the serializer for this notification type. '''
    @staticmethod
    def get_serializer():
        
        return 'ContractNotificationSerializer'

    ''' Return an offer notification serialized. '''
    @property
    def serialized(self):
        
        from kuser.serializers import ContractNotificationSerializer
        return ContractNotificationSerializer(self).data

