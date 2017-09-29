from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendr.settings')
app = Celery('vendr')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Application schedule.
app.conf.beat_schedule = {

        # Check for properties to unfeature every 2 hours.
        'property_unfeature': {
            'task': 'kproperty.tasks.property_unfeature_task',
            'schedule': crontab(hour='*/2')
        },
        
        # Check for open houses to clear every 2 hours.
        'openhouse_clear': {
            'task': 'kproperty.tasks.openhouse_clear_task',
            'schedule': crontab(hour='*/2')
        },

        # Notify anyone who has rsvp'd to an open house that
        # is starting soon.
        'openhouse_start': {
            'task': 'kproperty.tasks.openhouse_start',
            'schedule': crontab(minute='*/15')
        }
}

