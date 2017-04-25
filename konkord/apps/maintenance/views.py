# django imports
from maintenance.models import MaintenanceMessage
from django.template.loader import render_to_string
from core.decorators import ajax_required
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
import json


@ajax_required
def maintenance_messages(
        request,
        template_name="maintenance/maintenance_messages.html"):
    messages = MaintenanceMessage.objects.filter(
        start_time__lt=timezone.now()
    ).filter(
        Q(end_time__gte=timezone.now()) |
        Q(end_time__isnull=True),
    ).filter(Q(type=5) | Q(type=10))
    html = render_to_string(
        template_name, {'maintenance_messages': messages},
        request
    )
    response = json.dumps({'html': html})
    return HttpResponse(response)
