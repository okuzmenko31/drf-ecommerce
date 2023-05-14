import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery(__name__)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_expired_tokens_from_db': {
        'task': 'apps.users.tasks.delete_expired_tokens',
        'schedule': crontab(minute='*/1')
    }
}
