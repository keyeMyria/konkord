from .models import Filter
from django.shortcuts import Http404
from .settings import (
    PRICE, PROPERTY, STATUS
)
from _collections import defaultdict


def filter_products(products, filters, sorting):
    excluded_filters = ['sorting', 'pdf', 'page']
    for excluded_filter in excluded_filters:
        filters.pop(excluded_filter, None)
    if not filters:
        return products, {}
    filters_objects = Filter.objects.filter(slug__in=filters.keys())
    active_filters = defaultdict(list)
    if not filters_objects:
        raise Http404
    for filter_obj in filters_objects:
        if filter_obj.realization_type in (PROPERTY, STATUS):
            filter_values = filters[filter_obj.slug].split(',')
            options = filter_obj.filter_options.active().filter(
                value__in=filter_values
            ).values('id', 'name', 'value')
            options_count = options.count()
            if not options_count or options_count != len(filter_values):
                raise Http404
            for fo in options:
                active_filters[filter_obj.slug].append({
                    'name': fo['name'],
                    'value': fo['value'],
                    'filter_name': filter_obj.name
                })
                products = products.filter(filter_options__id=fo['id'])
        elif filter_obj.realization_type == PRICE:
            try:
                min_price, max_price = filters[filter_obj.slug].split('..')
                if min_price:
                    products = products.filter(price__gte=int(min_price))
                if max_price:
                    products = products.filter(price__lte=int(max_price))
            except:
                raise Http404
    products = products.distinct()
    if sorting:
        products = products.order_by(sorting)
    return products, active_filters


def generate_filters():
    for f in Filter.objects.all():
        f.parse(update_only=True)
