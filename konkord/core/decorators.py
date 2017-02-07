# coding: utf-8
from django.http import HttpResponseForbidden
from django.utils.safestring import mark_safe


_ERROR_MSG = '''
<!DOCTYPE html><html lang="en"><body><h1>%s</h1><p>%%s</p></body></html>
'''
_403_ERROR = _ERROR_MSG % '403 Forbidden'


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """
    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseForbidden(
                    mark_safe(_403_ERROR % 'Request must be set via AJAX.'))
            return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap