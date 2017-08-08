#
# Chat models.
#
# ==============================================================================

import uuid
import redis
import json

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


'''   These models are essentially containers for messages. Each chat has
      a set containing an arbitrary number of participants (users). '''
class Chat(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Message(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(Chat, related_name='messages',
            on_delete=models.CASCADE)
    
    # Soft reference to the sender. N.B. -- This is our chosen user
    # representation and, as such, is subject to change.
    sender = models.PositiveIntegerField(editable=False)
    
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    ''' A minimal message representation used for instant message alerts. '''
    @property
    def alert(self):
        return { 'sender': self.sender, 'content': self.content }

    ''' There are two behaviors we need to enforce on message saves:
        1. Immutability (i.e. prevent any edits).
        2. Notifications for the recipient. We'll use our trusty Redis queue here.
    '''
    def save(self, *args, **kwargs):
        
        if self._state.adding:
            self.publish()
            super(Message, self).save(*args, **kwargs)
    
    ''' Push our message into the appropriate channels. '''
    def publish(self):

            # Create a list of the other participant's channels.
            channels = [
                            'users.{}.inbox'.format(recipient.pk)
                            for recipient in self.chat.participants.all()
                            if recipient.pk != self.sender
            ]
            
            # Push our message alert to the appropriate channels.
            message_json = json.dumps(self.alert)
            r = redis.StrictRedis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT, db=0)
            
            for channel in channels:
                r.publish(channel, message_json)
   
