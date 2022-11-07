import os
from celery import Celery
from celery.schedules import crontab

import redis

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')

app = Celery('News_Portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_posts_notification': {
        'task': 'news.tasks.week_news_notification',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

red = redis.Redis(
    host='redis-18233.c251.east-us-mz.azure.cloud.redislabs.com',
    port=18233,
    password='ZgDKLcRhuUjTVdFAwuxM7xl4YMGii2jP'
)

