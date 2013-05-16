# -*- coding: utf-8 -*-

# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Copyright (C) 2012 Yahoo! Inc. All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc
import uuid

from oslo.config import cfg

"""Define APIs for the logbook providers."""

from nova.openstack.common import importutils
from nova.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class RecordNotFound(Exception):
    pass


class LogBook(object):
    """Base class for what a logbook (distributed or local or in-between)
    should provide"""

    __metaclass__ = abc.ABCMeta

    def __init__(self, resource_uri):
        self.uri = resource_uri

    @abc.abstractmethod
    def register_workflow(self, wf_name):
        """Atomically adds a new entry for workflows in the logbook"""
        #Check wfs already saved in logbook
        #Make sure wf_name doesn't overwrite a previous name
        #Save wf
        raise NotImplementedError()   

    @abc.abstractmethod
    def update_task(self, wf_name, task_name, **kwargs):
        """Registers a task to a given workflow"""
        # Pull wf from DB
        # make sure wf exists
        # if task name already exists, check instance # and increment
        # add task to wf with args
        # write task back to DB
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_workflow(self, wf_name):
        """Remove WF from DB after WF completion or otherwise"""
        # Check to see all tasks in WF are success
        # if not LOG.warning("WARNING: Not all tasks have completed!")
        # Remove WF from logbook
        raise NotImplementedError()

    def close(self):
        """Allows the job board provider to free any resources that it has."""
        pass


class DBLogBook(LogBook):
    """Base class for a logbook impl that uses a backing database."""

    def __init__(self, context, job):
        super(DBLogBook, self).__init__(job.uri)
        self.context = context
        self.job = job

    def close(self):
        # Free the db connection
        pass


class MemoryLogBook(LogBook):
    pass
