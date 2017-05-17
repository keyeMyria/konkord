from django import template
from ..models import Filter, FilterOption
from catalog.models import Product
from ..settings import PRICE
from django.db.models import Count, Min, Max, Q
from collections import OrderedDict, defaultdict
from django.conf import settings
from catalog.settings import GROUP_PRODUCTS_BY_PARENT
register = template.Library()


@register.inclusion_tag('filters/filters.html', takes_context=True)
def filters_block(context, products):
    request = context.get('request')
    if request is None:
        return {}
    selected_products_query = {
        'parent_id__in' if GROUP_PRODUCTS_BY_PARENT else 'id__in':
            list(products.values_list('id', flat=True))
    }
    params = {
        filter_slug: set(params.split(','))
        for filter_slug, params in request.GET.copy().items()
    }
    filters = OrderedDict()
    for f_slug in Filter.objects.values_list('slug', flat=True):
        filters[f_slug] = None

    selected_fos = set()
    not_selected_fos = []
    selected_filters = {}
    not_selected_filters = set()
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
            if fo.filter.id not in selected_filters:
                selected_filters[fo.filter.id] = [fo.id]
            else:
                selected_filters[fo.filter.id].append(fo.id)
            selected_fos.add(fo.id)
            filters[fo.filter.slug]['filter'].selected = True
        else:
            fo.selected = False
            not_selected_filters.add(fo.filter.id)
            not_selected_fos.append(fo.id)
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
                price_products = Product.objects.all()
                for fos_ids in selected_filters.values():
                    price_products = price_products.filter(
                        filter_options__id__in=fos_ids)
                aggregated_price = price_products.aggregate(
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
    additions = {}
    for selected_filter, filter_fos in selected_filters.items():
        filter_products = Product.objects.variants().filter(
            filter_options__filter_id=selected_filter
        ).filter(**price_filter)
        for fo in filter_fos:
            filter_products = filter_products.exclude(filter_options__id=fo)
        fos_without_curr_filter = selected_filters.copy()
        fos_without_curr_filter.pop(selected_filter)
        for fos in fos_without_curr_filter.values():
            filter_products = filter_products.filter(
                filter_options__id__in=fos)
        for fo_id, fo_quantity in filter_products.annotate(
            quantity=Count('filter_options__id')
        ).order_by().values_list('filter_options__id', 'quantity'):
            if fo_id not in additions:
                additions[fo_id] = fo_quantity
            else:
                additions[fo_id] += fo_quantity
    not_selected_fos_products = Product.objects.filter(
        filter_options__filter_id__in=not_selected_filters
    ).filter(**selected_products_query)
    for fo_id, fo_quantity in not_selected_fos_products.values(
        'filter_options__id'
    ).annotate(
        quantity=Count('filter_options__id')
    ).order_by().values_list('filter_options__id', 'quantity').iterator():
        if fo_id not in additions:
            additions[fo_id] = fo_quantity
        else:
            additions[fo_id] += fo_quantity
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
