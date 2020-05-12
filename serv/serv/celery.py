import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'serv.settings')
app = Celery('serv') 
# Префикс для констант в settings
app.config_from_object('django.conf:settings', namespace='CELERY')
# автозапуск задач из файла tasks.py в каталоге при приложения
app.autodiscover_tasks()

# Запуск периодических заданий (crontab)
# документация Periodic Tasks
# https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html

"""
app.conf.beat_schedule = {
	'run-my-task-1': {
		'task': 'имя_приложения.tasks.my_task_1',
		'schedule': crontab(minute='*/10'), # каждые 10 min
	},
}

"""