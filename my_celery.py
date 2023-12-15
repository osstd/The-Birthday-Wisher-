from celery import Celery
from celery.schedules import crontab
import os

celery = Celery(
    'tasks',
    broker=os.environ.get('R_KEY'),
    include=['tasks'],
)

celery.conf.beat_schedule = {
    'send-email-task': {
        'task': 'tasks.send_email_task',
        'schedule': crontab(hour="7", minute='30', day_of_week='*')
    },
}
celery.conf.update(timezone='America/New_York')
celery.conf.result_backend = os.environ.get('R_KEY')
