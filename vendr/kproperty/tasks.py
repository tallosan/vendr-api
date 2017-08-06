from __future__ import absolute_import
from celery import shared_task

@shared_task
def unfeature(eta):

    return 'this task will be unfeatured in {}'.format(eta)

