from __future__ import absolute_import
from datetime import timedelta
from celery.schedules import crontab
import os
import socket

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

if (socket.gethostname() == "habu"):
    BROKER_URL = 'amqp://guest:guest@habu:5672//'
else:
    BROKER_URL = os.getenv('BROKER_URL', 'amqp://guest:guest@localhost:5672//')

CELERY_TASK_SERIALIZER = 'pickle'

CELERY_ACCEPT_CONTENT = ['pickle']

import socket
hostname = socket.gethostname()

if hostname in ["habu", "support"] :
    home = "/home/www-data"
elif os.environ.has_key('HOME'):
    home = os.getenv("HOME")
else:
    home = "/home/www-data"

CELERYBEAT_SCHEDULE = {

    'prune_data': {
        'task': 'biostar.celery.call_command',
        'schedule': timedelta(days=1),
        'kwargs': dict(name="prune_data")
    },

    'sitemap': {
        'task': 'biostar.celery.call_command',
        'schedule': timedelta(hours=6),
        'kwargs': dict(name="sitemap")
    },

    'update_index': {
        'task': 'biostar.celery.call_command',
        'schedule': timedelta(minutes=15),
        'args': ["update_index"],
        'kwargs': {"age": 1}
    },

    'awards': {
        'task': 'biostar.celery.call_command',
        'schedule': timedelta(hours=3),
        'args': ["user_crawl"],
        'kwargs': {"award": True}
    },

    'hourly_dump': {
        'task': 'biostar.celery.call_command',
        'schedule': crontab(minute=10),
        'args': ["biostar_pg_dump"],
        'kwargs': {"hourly": True, "pg_user": "biostar",
            "outdir": os.path.join(home, "data")}
    },

    'daily_dump': {
        'task': 'biostar.celery.call_command',
        'schedule': crontab(hour=22),
        'args': ["biostar_pg_dump"],
        'kwargs': {"pg_user": "biostar",
            "outdir": os.path.join(home, "data")}
    },

    'hourly_feed': {
        'task': 'biostar.celery.call_command',
        'schedule': crontab(minute=10),
        'args': ["planet"],
        'kwargs': {"update": 1}
    },

    'daily_feed': {
        'task': 'biostar.celery.call_command',
        'schedule': crontab(hour='*/2', minute=15),
        'args': ["planet"],
        'kwargs': {"download": True}
    },

    # 'bump': {
    #     'task': 'biostar.celery.call_command',
    #     'schedule': timedelta(hours=6),
    #     'args': ["patch"],
    #     'kwargs': {"bump": True}
    # },

}

CELERY_TIMEZONE = 'UTC'
