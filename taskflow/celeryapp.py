import traceback as tb

from taskflow.tests import easy
from celery.signals import task_failure, task_success
from nova.openstack.common import log as logging

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
    wf = sender.name.split('.')[0]
    task = ('.').join(n for n in (sender.name.split('.')[1:]) if n)
    logbook.update_task(wf, task, status="ERROR", args=args, kwargs=kwargs,
                        exception=exception, traceback=(tb.print_tb(traceback)))
    
    # TODO: Auto-initiate rollback from failed task

@task_success.connect
def task_success_handler(singal=None, sender=None, result=None):
    """ Save task results to WF """
    wf = sender.name.split('.')[0]
    task = ('.').join(n for n in (sender.name.split('.')[1:]) if n)
    logbook.update_task(wf, task, status="SUCCESS", result=result)
    pass



