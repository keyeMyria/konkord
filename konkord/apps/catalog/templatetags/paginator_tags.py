# -*- coding: utf-8 -*-
from django.template import Library
from collections import deque
from itertools import count
import urllib

register = Library()


@register.simple_tag(takes_context=True)
def pagination_params(context, page):
    request = context.get('request')
    if not request:
        return ''
    get_params = request.GET.copy()
    if page == 1:
        get_params.pop('page', None)
    else:
        get_params['page'] = page
    return urllib.parse.unquote(get_params.urlencode())


@register.simple_tag()
def define_page_range(current_page, total_pages, window=6):
    """ Returns range of pages that contains current page and few pages
    before and after it.

        @current_page - starts from 1
        @tota_pages - total number of pages
        @window - maximum number of pages shown with current page - should
        be even

        Examples (cucumber style):
             Given window = 6
             When current_page is 8
             and total_pages = 20
             Then I should see: 5 6 7 [8] 9 10 11

             Given window = 6
             When current_page is 8
             and total_pages = 9
             Then I should see: 3 4 5 6 7 [8] 9

             Given window = 6
             When current_page is 1
             and total_pages = 9
             Then I should see: [1] 2 3 4 5 6 7
    """
    # maximum length of page range is window + 1
    maxlen = window + 1
    page_range = deque(maxlen=maxlen)

    # minimum possible index is either: (current_page - window) or 1
    window_start = (current_page - window) \
        if (current_page - window) > 0 else 1

    # maximum possible index is current_page + window or total_pages
    window_end = total_pages if (current_page + window) > \
        total_pages else (current_page + window)

    # if we have enough pages then we should end at preffered end
    preffered_end = current_page + int(window / 2.0)

    for i in count(window_start):
        if i > window_end:
            # if we're on first page then our window will be [1] 2 3 4 5 6 7
            break
        elif i > preffered_end and len(page_range) == maxlen:
            # if we have enough pages already then stop at preffered_end
            break
        page_range.append(i)
    return list(page_range)
