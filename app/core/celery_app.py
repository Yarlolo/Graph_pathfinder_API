from celery import Celery

celery_app = Celery(
    'tasks',
    broker="sqla+sqlite:///celery.db?check_same_thread=False",
    backend="db+sqlite:///results.db?check_same_thread=False",
    include=['app.services.graph'])

celery_app.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,)
