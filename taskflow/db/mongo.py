import pymongo
import logging
import functools

LOG = logging.getLogger(__name__)

class Driver(Base):

    def __init__(self, connection, db_driver=None):
        Base.__init__(self, connection, db_driver)
        self.db_name = "taskflow" #TODO: Make this configurable
        self._connection = None
        self._database = None
        self._client = None

    def database(self):
        """Connects to and returns mongo db object"""
        if self._database is None:
            if self._client is None:
                try:
                    self._client = (pymongo.MongoClient(self.connection))
                except pymongo.errors.AutoReconnect as exc:
                    LOG.error("Could not connect to DB: %s" % (exc,))
                    raise exc
             self._database = self._client[self.db_name]
             LOG.info("Connected to mongodb on %s" % (self.db_name,))

     def verify_workflow(self, wf_name):
         """ Checks to make sure wf_name is unique """
         if not self._client:
            self.database()
         client = self._client
         with client.start_request():
             names = database().collection_names()
             if wf_name in names:
                 msg = ("WF %s already exists." % (wf_name,))
                 LOG.error(msg)
                 raise Exception(msg)
             return True         

     def update_task(self, wf_name, task_name, **kwargs):
        """ Updates task in wf_name collection. Automatically
            inserts task if task has not been added yet """
        if not self._client:
            self.database()
        client = self._client
        for k, v in kwargs.items():
            with client.start_request():
                self.database()[wf_name].find_and_modify(
                    query={
                        'name': task_name
                    },
                    update={ $set: {
                        k: v
                    }},
                    upsert=True)
                LOG.info("Updated task %s with {%s:%s}" %
                         (task_name, k, v))
