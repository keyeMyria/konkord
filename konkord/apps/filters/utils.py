from .models import Filter
from django.shortcuts import Http404
from .settings import (
    PRICE, PROPERTY, STATUS
)
from catalog.models import Product


def filter_products(products, filters, sorting):
    filters.pop('sorting', None)
    filters.pop('pdf', None)
    filters_objects = Filter.objects.filter(slug__in=filters.keys())
    if not filters:
        return products
    if not filters_objects:
        raise Http404
    filter_options_ids = set([])
    for filter_obj in filters_objects:
        if filter_obj.realization_type in (PROPERTY, STATUS):
            options = filter_obj.filter_options.filter(
                value__in=filters[filter_obj.slug].split(',')
            ).values_list('id', flat=True)
            if not options:
                raise Http404
            filter_options_ids.update(set(options))
        elif filter_obj.realization_type == PRICE:
            try:
                min_price, max_price = filters[filter_obj.slug].split('..')
                if min_price:
                    products = products.filter(price__gte=int(min_price))
                if max_price:
                    products = products.filter(price__lte=int(max_price))
            except:
                raise Http404
    if filter_options_ids:  # only price filter active
        products = products.filter(
            filter_options__id__in=list(filter_options_ids))
    products_ids = products.order_by('id').distinct('id').values_list(
        'id', flat=True)
    products = Product.objects.filter(id__in=products_ids)
    if sorting:
        products = products.order_by(sorting)
    return products


def generate_filters():
    for filter in Filter.objects.all():
        filter.parse()