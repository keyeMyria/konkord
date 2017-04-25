# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView
from django.template.loader import render_to_string
from django.http import HttpResponse
from catalog.models import Product, ProductSorting
from core.utils import FilterProductEngine
from core.mixins import MetaMixin
import json
from pdf_pages.mixins import PDFPageMixin
from django.http.request import QueryDict
import urllib
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from . import settings as catalog_settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


@method_decorator(cache_page(60*60), 'dispatch')
@method_decorator(ensure_csrf_cookie, 'dispatch')
class MainPage(PDFPageMixin, MetaMixin, ListView):
    model = Product
    queryset = Product.objects.active()
    context_object_name = 'products'
    template_name = 'catalog/main_page.html'
    paginate_by = settings.CATALOG_PAGINATION_PRODUCTS_ON_PAGE
    active_filters = {}

    def get_queryset(self, page=1):
        queryset = super(MainPage, self).get_queryset()
        filters = self.kwargs.copy()
        for param in settings.CATALOG_IGNORED_FILTERS_PARAMS.split('\n'):
            filters.pop(param, None)
        filter_engine = FilterProductEngine()
        sorting = self.request.session.get('sorting', None) or\
            ProductSorting.objects.order_by('-position').first()
        products, self.active_filters = filter_engine.filter_products(
            queryset, filters, sorting)
        if catalog_settings.GROUP_PRODUCTS_BY_PARENT:
            return Product.objects.with_variants().filter(
                id__in=products.values_list('parent_id', flat=True)
            )
        else:
            return products

    def get(self, request, *args, **kwargs):
        get_copy = request.GET.copy()
        page = request.GET.get(self.page_kwarg)
        if page and int(page) == 1:
            get_copy.pop(self.page_kwarg)
            path = request.path
            querystring = urllib.parse.unquote(get_copy.urlencode())
            if querystring:
                path += '?' + querystring
            return redirect(path)
        self.kwargs.update( request.GET.dict())
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if page and int(page) > context['page_obj'].number:
            get_copy['page'] = context['page_obj'].number
            next_page = '?'.join([
                request.path,
                urllib.parse.unquote(get_copy.urlencode())
            ])
            return redirect(next_page)
        return self.render_to_response(context)

    def post(self, request):
        page_query = QueryDict(request.POST.get('next_page', ''), mutable=True)
        self.kwargs.update(page_query.dict())
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        html = render_to_string(
            'catalog/products.html', context
        )
        if context['page_obj'].has_next():
            page_number = context['page_obj'].next_page_number()
            page_query['page'] = page_number
            next_page = urllib.parse.unquote(page_query.urlencode())
        else:
            page_number = None
            next_page = None
        return HttpResponse(json.dumps({
            'products': html,
            'next_page': next_page,
            'page_number': page_number
        }))

    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumb_query = QueryDict(mutable=True)
        for filter_slug, options in self.active_filters.items():
            if len(options) == 1:
                option = options[0]
                breadcrumb_query[filter_slug] = option['value']
                breadcrumbs.append((
                    ' - '.join([option['filter_name'], option['name']]),
                    '?'.join([
                        self.request.path,
                        urllib.parse.unquote(
                            breadcrumb_query.urlencode())
                    ])
                ))
        return breadcrumbs

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset, if needed.
        """
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.request.GET.get(
            page_kwarg) or self.kwargs.get(page_kwarg) or 1
        try:
            page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page = paginator.page(paginator.num_pages)
        return paginator, page, page.object_list, page.has_other_pages()


@method_decorator(cache_page(60*60), 'dispatch')
@method_decorator(ensure_csrf_cookie, 'dispatch')
class ProductView(PDFPageMixin, MetaMixin, DetailView):
    methods = ['GET']
    model = Product
    queryset = Product.objects.active()
    template_name = 'catalog/product_detail.html'
    pdf_template = 'catalog/product_detail_pdf.html'

    def get_queryset(self):
        if catalog_settings.GROUP_PRODUCTS_BY_PARENT:
            return Product.objects.with_variants()
        else:
            return Product.objects.active()

    def get_breadcrumbs(self):
        obj = self.get_object()
        return [(obj.name, None)]

