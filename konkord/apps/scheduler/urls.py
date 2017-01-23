from django.conf.urls import url

from .views import (
    scheduler_state,
    edit_scheduling_job,
    scheduler_perform_job,
    scheduler_delete_job,
)

urlpatterns = [
    url(r'^$',
        scheduler_state, name='scheduler_home'),
    url(r'^(?P<job_id>[-\w]+)/scheduling/$',
        edit_scheduling_job, name='scheduler_edit_scheduling'),
    url(r'^(?P<job_id>[-\w]+)/perform/$',
        scheduler_perform_job, name='scheduler_perform'),
    url(r'^(?P<job_id>[-\w]+)/delete/$',
        scheduler_delete_job, name='scheduler_delete'),
]
