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

import sys
import abc


class Task(object):
    """An abstraction that defines a potential piece of work that can be
    applied and can be reverted to undo the work as a single unit.
    """
    # __metaclass__ = abc.ABCMeta

    def __str__(self):
        return "Task: %s" % (self.__class__.__name__)

    def __init__(self, apply, rollback=None):
        self._apply = apply
        self._rollback = rollback
        self._status = "NEW"
        self._children = []
        self._name = self.gen_task_name(apply)
        # self._name = apply.__name__

    def __call__(self, *args, **kwargs):
        self.apply(*args, **kwargs)    

    def gen_task_name(self, method):
        """Generate unique task name"""
        module = sys.modules[method.__module__]
        if module is not None:
            module_name = module.__name__
        method_name = method.__name__
        return '.'.join(n for n in (module_name, method_name) if n)
            

    def get_status(self):
        """Dynamically get task status stored in DB"""
        # driver.get_status(self._name)
        pass

    @abc.abstractmethod
    def apply(self, context, *args, **kwargs):
        """Activate a given task which will perform some operation and return.

           This method can be used to apply some given context and given set
           of args and kwargs to accomplish some goal. Note that the result
           that is returned needs to be serializable so that it can be passed
           back into this task if reverting is triggered."""
        raise NotImplementedError()

    def revert(self, context, result, cause):
        """Revert this task using the given context, result that the apply
           provided as well as any information which may have caused
           said reversion."""
        pass
