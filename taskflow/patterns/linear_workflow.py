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

# OrderedDict is only in 2.7 or greater :-(
if not hasattr(dict_provider, 'OrderedDict'):
    import ordereddict as dict_provider

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
        # Ordered dicts are used so that we can nicely refer to the tasks by
        # name and easily fetch their results but also allow for the running
        # of said tasks to happen in a linear order.
        self.tasks = []
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
        self.tasks.append(task)
        if( len(self.tasks) == 1):
            # set pointer to first task in workflow
            self.root = task.s(*args, **kwargs)
        else:
            # link tasks together
            self.tasks[-2].link(task.s(*args, **kwargs))

    def run(self, context, *args, **kwargs):
        """ Kick of root task """
        root(context)
    
    """
    def run(self, context, *args, **kwargs):
        for (name, task) in self.tasks.iteritems():
            try:
                self._on_task_start(context, task, name)
                # See if we have already ran this...
                result = None
                if self.result_fetcher:
                    result = self.result_fetcher(context, name, self)
                if result is None:
                    result = task.apply(context, *args, **kwargs)
                # Keep a pristine copy of the result in the results table
                # so that if said result is altered by other further states
                # the one here will not be.
                self.results[name] = copy.deepcopy(result)
                self._on_task_finish(context, task, name, result)
            except Exception as ex:
                with excutils.save_and_reraise_exception():
                    try:
                        self._on_task_error(context, task, name)
                    except Exception:
                        LOG.exception(_("Dropping exception catched when"
                                        " notifying about existing task"
                                        " exception."))
                    self.rollback(context,
                                  workflow.Failure(task, name, self, ex))

    def _on_task_error(self, context, task, name):
        # Notify any listeners that the task has errored.
        for i in self.listeners:
            i.notify(context, workflow.ERRORED, self, task, name)

    def _on_task_start(self, context, task, name):
        # Notify any listeners that we are about to start the given task.
        for i in self.listeners:
            i.notify(context, workflow.STARTING, self, task, name)

    def _on_task_finish(self, context, task, name, result):
        # Notify any listeners that we are finishing the given task.
        self.reversions.append((name, task))
        for i in self.listeners:
            i.notify(context, workflow.COMPLETED, self, task,
                     name, result=result)

    def rollback(self, context, cause):
        for (i, (name, task)) in enumerate(reversed(self.reversions)):
            try:
                task.revert(context, self.results[name], cause)
            except Exception:
                # Ex: WARN: Failed rolling back stage 1 (validate_request) of
                #           chain validation due to Y exception.
                msg = _("Failed rolling back stage %(index)s (%(name)s)"
                        " of workflow %(workflow)s, due to inner exception.")
                LOG.warn(msg % {'index': (i + 1), 'stage': name,
                         'workflow': self.name})
                if not self.tolerant:
                    # NOTE(harlowja): LOG a msg AND re-raise the exception if
                    # the chain does not tolerate exceptions happening in the
                    # rollback method.
                    raise
        if self.parents:
            # Rollback any parents workflows if they exist...
            for p in self.parents:
                p.rollback(context, cause)

    """
    
