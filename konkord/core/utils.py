# -*- coding: utf-8 -*-
from django.conf import settings
from django.core import urlresolvers
import importlib


def symbol_import(name):
    components = name.split('.')
    mod = importlib.import_module('.'.join(components[:-1]))
    func = getattr(mod, components[-1])
    return func


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
    print(obj)
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
