# -*- coding: utf-8 -*-
from django.conf import settings

TEMPLATES = (
    ('parent', u'Наследовать от родителя'),
    ('default.html', u'Стандартный шаблон'),
)

TEMPLATES += getattr(
    settings,
    'STATIC_PAGES_TEMPLATES',
    ()
)
