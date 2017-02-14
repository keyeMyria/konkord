from django import template
from ..models import Filter, FilterOption
from catalog.models import Product
from ..settings import CHECKBOX, RADIO, SELECT, SLIDER, PRICE
from django.db.models import Count
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
    filters = OrderedDict({})
    selected_fos = []
    price_filter = {}
    for f in Filter.objects.all().order_by('position'):
        filters[f.slug] = {
            'filter': f,
            'template': settings.FILTER_TEMPLATES[f.type],
            'options': []
        }
        if f.realization_type == PRICE:
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
    for fo in FilterOption.objects.all().order_by('position'):
        if fo.value in params.get(fo.filter.slug, []):
            fo.selected = True
            selected_fos.append(fo.id)
            filters[fo.filter.slug]['filter'].selected = True
        filters[fo.filter.slug]['options'].append(fo)
    additions = dict(Product.objects.exclude(
        filter_options__id__in=selected_fos
    ).filter(
        **price_filter
    ).values(
        'filter_options__id'
    ).annotate(
        quantity=Count('filter_options__id')
    ).order_by().values_list('filter_options__id', 'quantity'))

    return {'filters': filters, 'additions': additions, 'request': request}


@register.filter
def addition_for_fo(fo, additions):
    return additions.get(fo.id, 0)
