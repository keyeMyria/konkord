# coding: utf-8
import logging
import importlib
from django.conf import settings
import datetime

logger = logging.getLogger('sshop')


class BaseTaskQueue(object):
    queue_name = 'base'

    def schedule(
            self, function, sender=None, args=None,
            kwargs=None, priority=5, run_after=None, repeat=0):
        raise NotImplemented

    def deschedule(self, job_id):
        raise NotImplemented

    def check_status(self, job_id):
        raise NotImplemented

    def get_result(self, job_id):
        raise NotImplemented

    def get_pending_tasks(self, regex=None):
        raise NotImplemented

    def get_task_instance(self, job_id):
        raise NotImplemented

    @staticmethod
    def _func_name(func):
        return '.'.join([func.__module__, func.__qualname__])


class RQTaskQueue(BaseTaskQueue):

    queue_name = 'django_rq'
    DEFAULT_QUEUE_NAME = 'default'
    DEFAULT_JOB_TIMEOUT = 1800

    def schedule(
            self, function, sender=None, args=None,
            kwargs=None, priority=5, run_after=None, repeat=0):
        import django_rq
        queue = django_rq.get_queue(self.DEFAULT_QUEUE_NAME)
        scheduler = django_rq.get_scheduler(self.DEFAULT_QUEUE_NAME)
        now = datetime.datetime.now()

        _args = args or []
        _kwargs = kwargs or {}

        if isinstance(function, str):
            func = importlib.import_module(function)
            func_name = function
        else:
            func = function
            func_name = self._func_name(function)
        print(func_name)

        if func_name in getattr(settings, 'TASK_NAME_EXCLUDES', []):
            return 0

        _allow_concatenate_args = getattr(func, 'allow_concatenate_args', None)
        _ignore_duplicate_args_when_concatenate = \
            getattr(func, 'ignore_duplicate_args_when_concatenate', None)

        queue_pending_jobs = \
            [x for x in queue.get_jobs() if x.func_name == func_name]
        scheduler_pending_jobs = \
            [x for x in scheduler.get_jobs() if x.func_name == func_name]

        if queue_pending_jobs or scheduler_pending_jobs:
            for j in queue_pending_jobs + scheduler_pending_jobs:
                if list(j.args) == _args and j.kwargs == _kwargs:
                    return j.id
                else:
                    if _allow_concatenate_args:
                        if _ignore_duplicate_args_when_concatenate:
                            t = list(set(list(j.args) + _args))
                        else:
                            t = list(j.args) + _args
                        _args = t[:]
                        j.args = tuple(_args)
                        # A little trick for RQ
                        j.description = j.get_call_string()
                        j.save()
                        return j.id

        if run_after or repeat:
            # Apply timedelta for run_after
            from datetime import timedelta

            # Use scheduler to run a job at specified time
            if repeat is None:
                _kwargs['timeout'] = self.DEFAULT_JOB_TIMEOUT
                _job = scheduler.enqueue_at(
                    run_after,
                    func,
                    *_args,
                    **_kwargs
                )
            else:
                _job = scheduler.schedule(
                    scheduled_time=run_after or now,
                    func=func,
                    args=_args,
                    kwargs=_kwargs,
                    interval=int(repeat)*60,  # convert minutes to seconds
                    repeat=None,  # repeat forever
                    timeout=self.DEFAULT_JOB_TIMEOUT,
                )
            return _job.id
        else:
            _job = queue.enqueue_call(
                func=func,
                args=_args,
                kwargs=_kwargs,
                timeout=self.DEFAULT_JOB_TIMEOUT,
            )
            return _job.id

    def deschedule(self, job_id):
        job = self.get_task_instance(job_id)
        if job:
            return job.delete()

    def check_status(self, job_id):
        job = self.get_task_instance(job_id)
        if job:
            return job.status

    def get_result(self, job_id):
        job = self.get_task_instance(job_id)
        return job.result

    def get_pending_tasks(self, regex=None):
        import django_rq
        queue = django_rq.get_queue(self.DEFAULT_QUEUE_NAME)
        scheduler = django_rq.get_scheduler(self.DEFAULT_QUEUE_NAME)

        if regex is None:
            return queue.get_job_ids() + [x.id for x in scheduler.get_jobs()]
        else:
            import re
            _ids = []
            _jobs = queue.get_jobs() + scheduler.get_jobs()
            for _job in _jobs:
                _s = re.search(regex, _job.func_name)
                if _s:
                    _ids.append(_job.id)
            return _ids

    def get_task_instance(self, job_id):
        import django_rq
        queue = django_rq.get_queue(self.DEFAULT_QUEUE_NAME)
        _job = queue.fetch_job(job_id)
        return _job
