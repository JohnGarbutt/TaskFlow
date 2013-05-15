""" Celery Configuration File """

LOG = logging.getLogger(__name__)

""" If ALWAYS_EAGER is set to true, Celery will execute synchronously """
if '--eager' in sys.argv:
    CELERY_ALWAYS_EAGER = True
else:
    CELERY_ALWAYS_EAGER = False


