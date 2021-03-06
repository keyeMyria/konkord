# -*- coding: utf-8 -*-
from django.conf import settings
import sys
from django.core import urlresolvers
import importlib
from django.utils.safestring import mark_safe


def symbol_import(name):
    components = name.split('.')
    mod = importlib.import_module('.'.join(components[:-1]))
    func = getattr(mod, components[-1])
    return func


def import_module(module):
    """Imports module with given dotted name.
    """
    try:
        module = sys.modules[module]
    except KeyError:
        __import__(module)
        module = sys.modules[module]
    return module


def import_symbol(symbol):
    """Imports symbol with given dotted name.
    """
    module_str, symbol_str = symbol.rsplit('.', 1)
    module = import_module(module_str)
    return getattr(module, symbol_str)


class FilterProductEngine(object):
    def __init__(self):
        filter_func = symbol_import(getattr(
            settings,
            'FILTER_PRODUCT_FUNCTION',
            'core.utils.default_filter_product'
        ))
        setattr(self, 'filter_products', filter_func)


def default_filter_product(products, filters, sorting):
    """
    Default function (example) for filtering products. This function
    doesn't do filtering. Only returning products.
    """
    return products


def _get_named_patterns():
    """Returns list of (pattern-name, pattern) tuples
    """
    resolver = urlresolvers.get_resolver(None)
    patterns = sorted([
        (key, value[0][0][0])
        for key, value in resolver.reverse_dict.items()
        if isinstance(key, str)
    ])
    return patterns


def check_pattern_exist(pattern, obj=None):
    """ Return True, if url `pattern` exist, else - False
    """
    from catalog.models import Product
    from static_pages.models import PageCategory

    all_patterns = [i[1] for i in _get_named_patterns()]

    if pattern in all_patterns or (pattern + '/') in all_patterns:
        return True

    try:
        product = Product.objects.get(slug=pattern)
        if isinstance(obj, Product) and obj.id == product.id:
            return False
        else:
            return True
    except Product.DoesNotExist:
        pass

    try:
        page_category = PageCategory.objects.get(slug=pattern)
        if isinstance(obj, PageCategory) and obj.id == page_category.id:
            return False
        else:
            return True
    except PageCategory.DoesNotExist:
        pass

    return False


def render_meta_info(text, data):
    try:
        from django.template import Context, Template
        context = Context(data)
        template = Template(text)
        return mark_safe(template.render(context))
    except Exception as e:
        if 'request' in context and context['request'].user.is_authenticated()\
                and context['request'].user.is_superuser:
            error = e
        else:
            error = ''
        return error


def add_to_suit_config_menu(target, models):
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured
    config_menu = settings.SUIT_CONFIG.get('MENU', [])
    for tab in config_menu:
        if tab['tag'] == target:
            tab['models'] += models
            break
    else:
        raise ImproperlyConfigured(
            f'suit config menu tab with tag {target} not found')
