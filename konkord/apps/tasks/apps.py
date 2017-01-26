from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = 'tasks'

    def ready(self):
        from tasks.api import RQTaskQueue
        from django.conf import settings
        settings.ACTIVE_TASK_QUEUE = RQTaskQueue()
