import logging
import taskflow.common.cfg

LOG = logging.getLogger()

CONF = cfg.CONF

class Base(object):
    """ DB driver is injected in the init method. """

    def __init__(self, db_driver=None):
        if not db_driver:
            db_driver = CONF.db_driver
        self.driver = driver
        

