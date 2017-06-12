from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect


class StartRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'GET':
            params = request.GET.copy()
            start = params.get('start')
            if start:
                params.pop('start', None)
                request.GET = params.copy()
                query = request.GET.urlencode()
                if query:
                    return HttpResponseRedirect(f'{request.path}?{query}')
                return HttpResponseRedirect(request.path)
        return None
