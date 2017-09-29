from __future__ import unicode_literals

from django.apps import AppConfig


class KpropertyConfig(AppConfig):
    name = 'kproperty'

    ''' Register our signals. '''
    def ready(self):
	import signals.dispatch
        
