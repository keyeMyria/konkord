# -*- coding: utf-8 -*-
from django.conf import settings
import sys


def symbol_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


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
    def __init__(self, *args, **kwargs):
        super(FilterProductEngine, self).__init__(*args, **kwargs)
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
