# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    args = ''
    help = 'Job to clear finished django-rq jobs'

    def handle(self, *args, **options):
        import django_rq
        from rq.registry import FinishedJobRegistry
        from rq.exceptions import NoSuchJobError
        from rq.job import Job
        from datetime import datetime, timedelta
        day_before_yesterday = datetime.now() - timedelta(days=2)
        for index, config in enumerate(django_rq.settings.QUEUES_LIST):
            queue = django_rq.queues.get_queue_by_index(index)
            registry = FinishedJobRegistry(queue.name, queue.connection)
            for job_id in registry.get_job_ids():
                try:
                    job = Job.fetch(job_id, connection=queue.connection)
                    # delete jobs older 2 days
                    if job.ended_at > day_before_yesterday:
                        continue
                except NoSuchJobError:
                    # for some reason job already deleted but job key exists
                    pass
                registry.connection.zrem(registry.key, job_id)

