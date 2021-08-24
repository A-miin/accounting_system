import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')
app.conf.broker_url = 'redis://localhost:6379/0'

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
'print_heey_now': {
        'task': 'main.tasks.test',
        'schedule': 3600,
    },
    'create_MembershipFee_objects':{
        'task': 'main.tasks.create_membership_fee',
        'schedule': crontab(hour=0, minute=0, day_of_month=1),

    }
}

app.conf.timezone = 'Asia/Bishkek'
