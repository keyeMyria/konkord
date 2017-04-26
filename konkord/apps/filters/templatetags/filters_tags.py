from django import template
from ..models import Filter, FilterOption
from catalog.models import Product
from ..settings import PRICE
from django.db.models import Count, Min, Max, Q
from collections import OrderedDict
from django.conf import settings
register = template.Library()


@register.inclusion_tag('filters/filters.html', takes_context=True)
def filters_block(context, products):
    request = context.get('request')
    if request is None:
        return {}
    params = {
        filter_slug: set(params.split(','))
        for filter_slug, params in request.GET.copy().items()
    }
    filters = OrderedDict()
    for f_slug in Filter.objects.values_list('slug', flat=True):
        filters[f_slug] = None

    selected_fos = []
    price_filter = {}
    for fo in FilterOption.objects.active().select_related('filter'):
        if fo.filter.slug not in filters or filters[fo.filter.slug] is None:
            filters[fo.filter.slug] = {
                'filter': fo.filter,
                'template': settings.FILTER_TEMPLATES[fo.filter.type],
                'options': []
            }
        if fo.value in params.get(fo.filter.slug, []):
            fo.selected = True
            selected_fos.append(fo.id)
            filters[fo.filter.slug]['filter'].selected = True
        if fo.popular:
            filters[fo.filter.slug]['filter'].has_popular_options = True
        filters[fo.filter.slug]['options'].append(fo)
    for f in Filter.objects.filter(realization_type=PRICE):
        filters[f.slug] = {
            'filter': f,
            'template': settings.FILTER_TEMPLATES[f.type],
            'options': []
        }
        if f.realization_type == PRICE:
            if selected_fos:
                products = Product.objects.all()
                for fo in selected_fos:
                    products = products.filter(filter_options__id=fo)
                aggregated_price = products.aggregate(
                    min_price=Min('price'), max_price=Max('price'))
                f.min_price, f.max_price = (
                    aggregated_price['min_price'] or 0,
                    aggregated_price['max_price'] or 0
                )
            min_selected_price, max_selected_price =\
                request.GET.get(f.slug, '..').split('..')
            filters[f.slug]['min_selected_price'] =\
                min_selected_price or f.min_price
            filters[f.slug]['max_selected_price'] =\
                max_selected_price or f.max_price
            if min_selected_price:
                price_filter['price__gte'] = min_selected_price
            if max_selected_price:
                price_filter['price__lte'] = max_selected_price
    additions = dict(Product.objects.exclude(
        filter_options__id__in=selected_fos
    ).filter(
        **price_filter
    ).values(
        'filter_options__id'
    ).annotate(
        quantity=Count('filter_options__id')
    ).order_by().values_list('filter_options__id', 'quantity'))
    res_filters = OrderedDict()

    for f_slug, f_data in filters.items():
        if f_data:
            res_filters[f_slug] = f_data

    return {
        'filters': res_filters,
        'additions': additions,
        'request': request,
        'show_clear_filters_button': bool(selected_fos) or price_filter
    }


@register.filter
def addition_for_fo(fo, additions):
    return additions.get(fo.id, 0)
