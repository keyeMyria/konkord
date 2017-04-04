from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.functions import Now
from django.utils.translation import ugettext_lazy as _


class SchedulerConfig(AppConfig):
    name = 'scheduler'
    verbose_name = _('Django RQ Scheduler')

    def ready(self):
        from django.conf import settings
        from core import add_to_suit_config_menu
        add_to_suit_config_menu(
            'tasks',
            (
                {
                    'url': 'scheduler_home',
                    'label': _('Scheduler state'),
                },
                'scheduler.repeatablejob',
                'scheduler.scheduledjob',
            )
        )
        try:
            self.reschedule_repeatable_jobs()
            self.reschedule_scheduled_jobs()
        except:
            # Django isn't ready yet, example a management command is being
            # executed
            pass
        from django.conf.urls import include, url
        settings.APPS_URLS.extend([
            url(r'^scheduler/', include('scheduler.urls'))
        ])

    def reschedule_repeatable_jobs(self):
        repeatable_job = self.get_model('RepeatableJob')
        jobs = repeatable_job.objects.filter(enabled=True)
        self.reschedule_jobs(jobs)

    def reschedule_scheduled_jobs(self):
        scheduled_job = self.get_model('ScheduledJob')
        jobs = scheduled_job.objects.filter(
            enabled=True, scheduled_time__lte=Now())
        self.reschedule_jobs(jobs)

    def reschedule_jobs(self, jobs):
        for job in jobs:
            if job.is_scheduled() is False:
                job.save()
