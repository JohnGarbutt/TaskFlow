import logging
import abc

import taskflow.common.cfg

LOG = logging.getLogger()

CONF = cfg.CONF

class Base(object):
    """ DB driver is injected in the init method. """

    __metaclass__ = abc.ABCMeta

    def __init__(self, connection, db_driver=None):
        self.connection = connection
        self.driver = driver

    """
    def save_workflow(self, wf_name):
        """Save WF to DB"""
        raise NotImplementedError()
    """

    def save_task(self, wf_name, task_name):
        """Save Task to WF in DB"""
        raise NotImplementedError()

    def update_task(self, wf_name, task_name, task_data):
        """Update task with given task_data"""
        raise NotImplementedError()
