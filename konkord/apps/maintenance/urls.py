from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^messages/$',
        views.maintenance_messages, name="maintenance_messages"),
]
