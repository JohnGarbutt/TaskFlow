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

import collections as dict_provider
import copy

from nova import workflow
from nova.openstack.common import excutils
from nova.openstack.common import log as logging

LOG = logging.getLogger(__name__)


class Workflow(object):
    """A linear chain of independent tasks that can be applied as one unit or
       rolled back as one unit."""

    def __init__(self, name, tolerant=False, parents=None):
        # The tasks which have been applied will be collected here so that they
        # can be reverted in the correct order on failure.
        self.reversions = []
        self.name = name
        # If this chain can ignore individual task reversion failure then this
        # should be set to true, instead of the default value of false.
        self.tolerant = tolerant
        self.results = []
        self.root = None
        # If this workflow has a parent workflow/s which need to be reverted if
        # this workflow fails then please include them here to allow this child
        # to call the parents...
        self.parents = parents
        # This should be a functor that returns whether a given task has
        # already ran by returning the return value of the task or returning
        # 'None' if the task has not ran.
        #
        # NOTE(harlowja): This allows for resumption by skipping tasks which
        # have already occurred. The previous return value is needed due to
        # the contract we have with tasks that they will be given the value
        # they returned if reversion is triggered.
        self.result_fetcher = None
        # Any objects that want to listen when a task starts/stops/completes
        # or errors should be registered here. This can be used to monitor
        # progress and record tasks finishing (so that it becomes possible to
        # store the result of a task in some persistent or semi-persistent
        # storage backend).
        self.listeners = []


    def chain(self, task, *args, **kwargs):
        """ Chain task to end of end of workflow """
        # Register task to WF in logbook
        logbook.register_task(self.name, task.name)
        # Link task name to WF
        task.name = '%s.%s' % (self.name, task.name)
        self.tasks.append(task)
        if( len(self.tasks) == 1):
            # set pointer to first task in workflow
            self.root = task.s(*args, **kwargs)
            LOG.info('WF %s root task set to %s' % (self.name, task.name))
        else:
            # Set following task as a callback for preceding task
            self.tasks[-2].link(task.s(*args, **kwargs))

    def run(self, context, *args, **kwargs):
        """ Start root task and kick off workflow """
        root(context)
        LOG.info('WF %s has been started' % (self.name,))

    def set_result(self, task, 
 
