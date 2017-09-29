#
# Notification models.
#
# ==========================================================================

from __future__ import unicode_literals

import uuid
import redis
import json

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_delete
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.dispatch import receiver

from vendr_core.dispatch import receiver_extended
from transaction.models import Transaction, Offer, Contract
from transaction.models import HouseContract, CoOpContract, CondoContract, \
        TownhouseContract, ManufacturedContract, VacantLandContract
from transaction.models import CompletionDateClause, IrrevocabilityClause, \
        MortgageDeadlineClause, SurveyDeadlineClause, DepositClause, \
        ChattelsAndFixsClause, BuyerArrangesMortgageClause, EquipmentClause, \
        EnvironmentClause, MaintenanceClause, UFFIClause, PaymentMethodClause, \
        ChattelsIncludedClause, FixturesExcludedClause, RentalItemsClause

CONTRACTS = [HouseContract, CoOpContract, CondoContract, TownhouseContract,
        ManufacturedContract, VacantLandContract]
CLAUSES = [CompletionDateClause, IrrevocabilityClause, MortgageDeadlineClause,
        SurveyDeadlineClause, DepositClause, ChattelsAndFixsClause,
        BuyerArrangesMortgageClause, EquipmentClause, EnvironmentClause,
        MaintenanceClause, UFFIClause, PaymentMethodClause, ChattelsIncludedClause,
        FixturesExcludedClause, RentalItemsClause]


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
@receiver_extended(signals=[post_save, post_delete], senders=CONTRACTS)
@receiver_extended(signals=[post_save, post_delete], senders=CLAUSES)
def handler(sender, instance, **kwargs):
    
    notification_type = resolve_type(instance.__class__)

    # Creation notification. Note, we need to ensure that the sender was just created.
    if (kwargs['signal'] == post_save) and (kwargs['created']):
        notification = notification_type.objects.create_creation_notification(instance)
    
    # Update notification.
    elif (kwargs['signal'] == post_save) and (not kwargs['created']):
        notification = notification_type.objects.create_update_notifiation(instance)

    # Deletion notification.
    elif kwargs['signal'] == post_delete:
        notification = notification_type.objects.create_deletion_notification(instance)
    
    # Publish to our Redis server iff a notification was created.
    if not notification: return

    channel = 'users.{}.notifications'.format(notification.recipient.pk)
    notification_json = json.dumps(notification.serialized)
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    r.publish(channel, notification_json)


''' Determine the notification type for the given sender.
    Args:
        instance_class: The model that sent the notification.
'''
def resolve_type(sender_class):

    if sender_class in CONTRACTS: return ContractNotification
    elif sender_class in CLAUSES: return DynamicClauseNotification

    class_mappings = {
                        Offer: OfferNotification,
    }

    return class_mappings[sender_class]


'''   Abstract Base notification manager. '''
class BaseNotificationManager(models.Manager):

    ''' [Abstract] Notification for instance creation. Children must implement this. '''
    def create_creation_notification(self, instance):
        raise NotImplementedError('error: all notifications must implement this.')

    ''' [Abstract] Notification for instance deletion. Children must implement this. '''
    def create_deletion_notification(self, instance):
        raise NotImplementedError('error: all notifications must implement this.')


'''   Abstract manager for transaction related notifications. '''
class TransactionNotificationManager(BaseNotificationManager):
    
    resource = None

    ''' [Abstract] Create a creation transaction notification for a given resource. '''
    def create_creation_notification(self, instance):
        
        transaction = instance.transaction
        
        # Deterimine the notification's recipient, and format its description.
        recipient   = transaction.buyer if (instance.owner == transaction.seller) \
                                      else transaction.seller
        sender      = instance.owner.profile.first_name
        description = '{} has sent you a new {} on your property {}.'.format(
                       sender, self.resource, transaction.kproperty.location.address)
        
        # Create the notification.
        create_kwargs = {
                            'recipient': recipient, 'sender': sender,
                            'description': description,
                            'transaction': transaction.pk,
                            self.resource: instance.pk
        }
        notification = self.create(**create_kwargs)
        
        return notification
    
    ''' [Abstract] Create a deletion transaction notification for a given resource. '''
    def create_deletion_notification(self, instance):
        
        transaction = instance.transaction
        recipient   = transaction.buyer if (instance.owner == transaction.seller) \
                                        else transaction.seller
        sender      = instance.owner.profile.first_name
        description = '{} has withdrawn their {} on your property {}.'.format(
                       sender, self.resource, str(transaction.kproperty))
        
        # Create the notification.
        create_kwargs = {
                            'recipient': recipient, 'sender': sender,
                            'description': description,
                            'transaction': transaction.pk,
                            self.resource: instance.pk
        }
        
        notification = self.create(**create_kwargs)

        return notification


'''   Responsible for creating all types of offer notifications.'''
class OfferNotificationManager(TransactionNotificationManager):

    resource = 'offer'
    
    ''' Notification on Offer deletion. Note, we will need to determine if the offer's
        transaction is dampening the signal. As we use a cascading delete for
        transaction offers, the default signal behavior will create a new deletion offer
        for each offer in the transaction. What we want is for ONLY the most recent
        offer to send a notification, with the others deleting silently. To do this,
        we check if an offer has fired a signal and, if it has, we dampen the signal
        so that subsequent offer deletions do not create notifications.
        Args:
            instance: The Offer being deleted.
    '''
    def create_deletion_notification(self, instance):
        
        transaction = instance.transaction
        if transaction._dampen and transaction._fired:
            return
        elif transaction._dampen and (not transaction._fired):
            transaction._fired = True; transaction.save()

        return super(OfferNotificationManager, self).\
               create_deletion_notification(instance)


'''   Contract notification manager. '''
class ContractNotificationManager(TransactionNotificationManager):

    resource = 'contract'


class DynamicClauseNotificationManager(BaseNotificationManager):

    resource = 'clause'

    ''' [Abstract] Notification for instance creation. Children must implement this. '''
    def create_creation_notification(self, instance):
        return

    ''' [Abstract] Notification for instance deletion. Children must implement this. '''
    def create_deletion_notification(self, instance):
        return
   

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
    actual_type   = GenericForeignKey('_content_type', 'id')

    class Meta:
        abstract = True

    ''' Custom save method. Sets actual type value. '''
    def save(self, *args, **kwargs):
        
        # Set the actual type if we're creating the model.
        if self._state.adding:
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

    offer = models.UUIDField()
    _type = models.CharField(default='offer', max_length=5, editable=False)
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
    _type = models.CharField(default='contract', max_length=8, editable=False)
    objects = ContractNotificationManager()
    
    ''' Returns the serializer for this notification type. '''
    @staticmethod
    def get_serializer():
        
        return 'ContractNotificationSerializer'

    ''' Return an offer notification serialized. '''
    @property
    def serialized(self):
        
        from kuser.serializers import ContractNotificationSerializer
        return ContractNotificationSerializer(self).data


'''   A notification on a transaction contract's clause. '''
class DynamicClauseNotification(ContractNotification):

    clause  = models.UUIDField()
    objects = DynamicClauseNotificationManager()

    ''' Return a clause notification serialized. '''
    @property
    def serialized(self):
        pass


class OpenHouseStartNotification(BaseNotification):

    _type = models.CharField(default='openhouse_start', max_length=15, editable=False)
    recipient   = models.ForeignKey(settings.AUTH_USER_MODEL,
                    related_name='openhouse_notifications', on_delete=models.CASCADE)
    openhouse_owner = models.CharField(default='openhouse_owner',
            max_length=20, editable=False)
    openhouse_address = models.CharField(default='kproperty',
            max_length=35, editable=False)

    def save(self, *args, **kwargs):

        if self._state.adding:
            self.description = "Hey {}, just a reminder that the open house " \
                "on {}'s home at {} is starting in an hour!".format(
                        self.recipient.profile.first_name,
                        self.openhouse_owner,
                        self.openhouse_address
            )

        super(OpenHouseStartNotification, self).save(*args, **kwargs)
    
    """ A serialized representation of the notification. """
    @property
    def serialized(self):

        from kuser.serializers import OpenHouseStartNotificaitonSerializer
        return OpenHouseStartNotificaitonSerializer(self).data

    """ Returns the serializer for this notification type. """
    @staticmethod
    def get_serializer():
        return 'OpenHouseStartNotificaitonSerializer'

    """ Publish the notification to the appropriate channel. """
    def publish(self):

        channel = 'users.{}.notifications'.format(self.recipient.pk)
        notification_json = json.dumps(self.serialized)
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
        r.publish(channel, notification_json)

