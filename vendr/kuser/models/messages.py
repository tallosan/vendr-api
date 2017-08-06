#
# Messaging framework.
#
# ==============================================================================

import uuid
import redis
import json

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Message(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    convo = models.ForeignKey(Chat, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    ''' A serialized version of our message. '''
    @property
    def serialized(self):
        return

    ''' There are two behaviors we need to enforce on message saves:
        1. Immutability (i.e. prevent any edits).
        2. Notifications for the recipient. We'll use our trusty Redis queue here.
    '''
    def save(self, *args, **kwargs):
        
        if not self.pk:
            super(Message, self).save(*args, **kwargs)
            
            # Get a list of channels to push our message to.
            # N.B. -- We do not want/need to push to the sender's inbox, so we'll
            # tactfully exclude their channel from our list.
            channels = [
                            'users.{}.inbox'.format(recipient.pk)
                            for recipient in self.convo.participants
                            if recipient.pk != sender.pk
            ]
            
            # Push our message to the appropriate channels.
            message_json = json.dumps(message.serialized)
            r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
            for channel in channels:
                r.publish(channel, message_json)
   

class Convo(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ArrayField(models.UUIDField())

    # TODO:
    #
    #    The messaging flow is this:
    #
    #    1. Alice wants to talk to James.
    #    -- Alice POSTs a Convo to James.
    #
    #    2. If Alice is not blocked, then the Convo will be created.
    #    -- Alice & James can now POST Messages to the Convo resource endpoint.
    #
    #    3. Finis.
    #

