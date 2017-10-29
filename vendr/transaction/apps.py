from __future__ import unicode_literals

from django.apps import AppConfig


class TransactionConfig(AppConfig):
    name = 'transaction'
    
    """ Register our signals. """
    def ready(self):
        import signals.dispatch

