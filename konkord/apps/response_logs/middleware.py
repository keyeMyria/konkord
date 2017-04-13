# coding: utf-8
from django.utils.deprecation import MiddlewareMixin


class ResponseLogMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        from .models import ResponseLog
        if response.status_code in [301, 404]:
            url = request.build_absolute_uri()
            obj, created = ResponseLog.objects.get_or_create(
                url=url,
                referer=request.META.get('HTTP_REFERER', 'empty_referer'),
                status_code=response.status_code
            )
            obj.count += 1
            obj.save()
        return response
