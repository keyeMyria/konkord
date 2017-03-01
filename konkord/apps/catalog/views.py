# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView
from django.template.loader import render_to_string
from django.http import HttpResponse
from catalog.models import Product, ProductSorting
from core.utils import FilterProductEngine
from core.mixins import MetaMixin
import json
from django.template import RequestContext
from pdf_pages.mixins import PDFPageMixin
from django.http.request import QueryDict
import urllib
from django.conf import settings


class MainPage(PDFPageMixin, MetaMixin, ListView):
    model = Product
    queryset = Product.objects.active()
    context_object_name = 'products'
    template_name = 'catalog/main_page.html'
    paginate_by = 20

    def get_queryset(self, page=1):
        queryset = super(MainPage, self).get_queryset()
        filters = self.kwargs.copy()
        for param in settings.CATALOG_IGNORED_FILTERS_PARAMS.split('\n'):
            filters.pop(param, None)
        filter_engine = FilterProductEngine()
        sorting = self.request.session.get('sorting', None) or\
            ProductSorting.objects.order_by('-position').first()
        products = filter_engine.filter_products(queryset, filters, sorting)
        return Product.objects.with_variants().filter(
            id__in=products.values_list('parent_id', flat=True))

    def get(self, request, *args, **kwargs):
        self.kwargs.update(request.GET.dict())
        return super(MainPage, self).get(request, *args, **kwargs)

    def post(self, request):
        page_query = QueryDict(request.POST.get('next_page', ''), mutable=True)
        self.kwargs.update(page_query.dict())
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        html = render_to_string(
            'catalog/products.html', RequestContext(request, {
                'products': context['products'],
            })
        )
        if context['page_obj'].has_next():
            page_number = context['page_obj'].next_page_number()
            page_query['page'] = page_number
            next_page = urllib.parse.unquote(page_query.urlencode())
        else:
            next_page = None
        return HttpResponse(json.dumps({
            'products': html,
            'next_page': next_page
        }))


class ProductView(PDFPageMixin, MetaMixin, DetailView):
    methods = ['GET']
    model = Product
    queryset = Product.objects.active()
    template_name = 'catalog/product_detail.html'
    pdf_template = 'catalog/product_detail_pdf.html'

    def get_breadcrumbs(self):
        obj = self.get_object()
        return [(obj.name, None)]

