# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import get_language


def search(request):
    return {
        'search_input_placeholder': getattr(
            settings, 'SEARCH_INPUT_PLACEHOLDER_' + get_language().upper()),
    }
