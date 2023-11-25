from __future__ import absolute_import

from celery import shared_task


# Example of celery usage
@shared_task(name="apps.util.tasks.test")
def test(param):
    return 'The tasks executed with the following parameter: "%s"' % param
