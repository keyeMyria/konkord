import datetime
import pytz
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from .forms import JobSchedulingForm
from django_rq.queues import get_connection
from rq.job import Job


@staff_member_required
def scheduler_state(request):
    import django_rq
    scheduler = django_rq.get_scheduler('default')

    jobs = scheduler.get_jobs()

    with scheduler.connection._pipeline() as pipe:
        for j in jobs:
            pipe.watch(scheduler.scheduled_jobs_key)
            _unixtime = pipe.zscore(scheduler.scheduled_jobs_key, j.id)
            if _unixtime is not None:
                _time = datetime.datetime.fromtimestamp(_unixtime)
                j.scheduled_time = _time
            else:
                j.scheduled_time = None

            if j.enqueued_at is not None:
                j.enqueued_at = pytz.timezone('utc').localize(j.enqueued_at)
            if j.started_at is not None:
                j.started_at = pytz.timezone('utc').localize(j.started_at)
            if j.ended_at is not None:
                j.ended_at = pytz.timezone('utc').localize(j.ended_at)

            # convert seonds to minutes
            j.timeout_min = int(j.timeout / 60)
            j.interval_min = int(j.meta.get('interval') / 60)

    context_data = {
        'scheduler': scheduler,
        'jobs': jobs,
    }
    return render(request, 'scheduler/scheduler_state.html', context_data)


@staff_member_required
def edit_scheduling_job(request, job_id):
    import django_rq
    connection = get_connection()
    job = Job.fetch(job_id, connection=connection)
    queue = django_rq.get_queue('default')
    scheduler = django_rq.get_scheduler('default')
    job = queue.fetch_job(job_id)

    with scheduler.connection._pipeline() as pipe:
        pipe.watch(scheduler.scheduled_jobs_key)
        _unixtime = pipe.zscore(scheduler.scheduled_jobs_key, job.id)
        if _unixtime is not None:
            _time = datetime.datetime.fromtimestamp(_unixtime)
        else:
            _time = None

    if request.method == 'POST':
        form = JobSchedulingForm(request.POST)
        if form.is_valid():
            _next_time = form.cleaned_data['next_start']
            _next_unixtime = _next_time.timestamp()

            new_repeat = form.cleaned_data['repeat'] * 60
            new_timeout = form.cleaned_data['timeout'] * 60

            if _next_unixtime != _unixtime:
                with scheduler.connection._pipeline() as pipe:
                    pipe.watch(scheduler.scheduled_jobs_key)
                    pipe.zadd(
                        scheduler.scheduled_jobs_key, _next_unixtime, job.id)
            if new_repeat != job.meta.get('interval'):
                job.meta['interval'] = new_repeat
                job.save()
            if new_timeout != job.timeout:
                job.timeout = new_timeout
                job.save()
            return redirect(
                reverse('scheduler_edit_scheduling', args=[job.id]))
    else:
        form = JobSchedulingForm(initial={
            'next_start': _time,
            'repeat': int(job.meta.get('interval') / 60),
            'timeout': int(job.timeout / 60),
            })

    context_data = {
        'scheduler': scheduler,
        'job': job,
        'time': _time,
        'form': form,
        'timeout_min': int(job.timeout / 60),
        'interval_min': int(job.meta.get('interval') / 60),
    }
    return render(request, 'scheduler/edit_scheduling.html', context_data)


@staff_member_required
def scheduler_perform_job(request, job_id):
    import django_rq
    connection = get_connection()
    job = Job.fetch(job_id, connection=connection)
    queue = django_rq.get_queue(
        DJANGO_RQ_TASKS_QUEUES_MAPPING.get(job.func_name, 'default')
    )
    queue.enqueue_call(
        func=job.func_name,
        args=job.args,
        kwargs=job.kwargs,
    )
    return redirect(reverse('scheduler_home'))


@staff_member_required
def scheduler_delete_job(request, job_id):
    connection = get_connection()
    job = Job.fetch(job_id, connection=connection)
    job.delete()
    return redirect(reverse('scheduler_home'))
