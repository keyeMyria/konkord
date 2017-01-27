# -*- coding: utf-8 -*-
from django.conf import settings
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
