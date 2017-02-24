# -*- coding: utf-8 -*-
# from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
from search.models import SearchText
from search.utils import exclude_special_symbols
from catalog.models import Product
from search.serializers import LiveSearchSerializer
from django.conf import settings
from django.utils.translation import get_language
from core.mixins import MetaMixin
from django.utils.translation import ugettext_lazy as _


class SearchMixin(object):
    def get_queryset(self, *args, **kwargs):
        query_str = self.request.GET.get(
            'query',
            self.request.POST.get('query', None)
        )
        if not query_str:
            return Product.objects.none()
        language = get_language()
        query = {
            f'search_text_{language}__contains':
            exclude_special_symbols(query_str),
            'product__status__in_search': True
        }
        product_ids = SearchText.objects.filter(
            **query
        ).values_list('product__id').distinct()
        return Product.objects.filter(
            id__in=product_ids, status__in_search=True)


class SearchView(MetaMixin, SearchMixin, ListView):
    methods = ["POST", "GET"]
    context_object_name = 'products'
    model = Product
    queryset = Product.objects.in_search()
    template_name = 'search/results_list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get('query', None)
        # products = self.get_products(query)
        context.update({
            'query': query,
            # 'products': products
        })
        return context

    def post(self, request):
        query = self.request.POST.get('query', None)
        products = self.get_products(query)
        total_count = products.count()
        serializer = LiveSearchSerializer(
            products[:settings.LIVE_SEARCH_LIMIT], many=True)
        return JsonResponse({
            'products': serializer.data,
            'total_count': total_count,
            'query': query
        })

    def get_breadcrumbs(self):
        return [
            (_('Search'), None)
        ]
