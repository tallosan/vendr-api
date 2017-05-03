from __future__ import unicode_literals

from django.apps import AppConfig


class NotificationConfig(AppConfig):
    name = 'notification'

    ''' Register our Notification signals. '''
    def ready(self):
        
        from .models.notification import handler

