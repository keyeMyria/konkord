from django.views.generic import RedirectView
from django.core.cache import cache


class ClearCacheView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        cache.clear()
        return self.request.META.get('HTTP_REFERER')
