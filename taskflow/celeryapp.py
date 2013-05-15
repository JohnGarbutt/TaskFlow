import logging

import traceback as tb

from taskflow.tests import easy
from celery.signals import task_failure

LOG = logging.getLogger(__name__)

easy.register()

@task_failure.connect
def task_error_handler(signal=None, sender=None, task_id=None,
                       exception=None, args=None, kwargs=None,
                       traceback=None, einfo=None):
    """ If a task errors out, log all error info """
    LOG.error('Task %s, id: %s, called with args: %s, and kwargs: %s'
              'failed with exception: %s' % (sender.name, task_id,
                                             args, kwargs, exception))
    LOG.error('Trackeback: %s' % (tb.print_tb(traceback), ))
    # TODO: Auto-initiate rollback from failed task

@task_success.connect


