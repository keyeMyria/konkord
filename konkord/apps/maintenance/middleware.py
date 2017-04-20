# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from maintenance.models import MaintenanceMessage
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.urlresolvers import resolve
from django.core.cache import cache
from django.db.models import Q
from django.utils.deprecation import MiddlewareMixin


class MaintenanceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        messages = None
        if getattr(settings, 'MAINTENANCE_CACHE_MESSAGES', False):
            messages = cache.get('maintenance_messages')

        if not messages:
            messages = MaintenanceMessage.objects.filter(
                start_time__lt=timezone.now()).filter(
                    Q(end_time__gte=timezone.now()) |
                    Q(end_time__isnull=True))
            if getattr(settings, 'MAINTENANCE_CACHE_MESSAGES', False):
                cache.set(
                    'maintenance_messages',
                    messages,
                    getattr(settings, 'MAINTENANCE_CACHE_SECONDS', 3600))

        try:
            view, args, kwargs = resolve(request.path)
        except Exception:
            return None
        max_type = 0

        for m in messages:
            if m.type > max_type:
                max_type = m.type

        if getattr(settings, 'ADMIN_ROOT_PATH', '/admin') not in request.path \
                and messages.count() > 0:
            if max_type < 15 or request.user.is_superuser:
                request.maintenance_messages = messages
                request.max_maintenance_type = max_type
                return None
            else:
                template = render_to_string('maintenance/503.html', {
                    'title': _('Maintenance Mode'),
                    'messages': messages
                }, request)
                return HttpResponse(template, status=503)
        else:
            if messages.count() > 0:
                request.maintenance_messages = messages
                request.max_maintenance_type = max_type
                return None
            else:
                return None
