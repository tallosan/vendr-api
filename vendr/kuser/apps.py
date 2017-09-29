from __future__ import unicode_literals

from django.apps import AppConfig


class KuserConfig(AppConfig):
    name = 'kuser'

    ''' Register our Notification signals. '''
    def ready(self):

        from .models.notification import handler
        from .signals import *
        
