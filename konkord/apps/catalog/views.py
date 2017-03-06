# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template import RequestContext
from catalog.models import Product, ProductSorting
from core.utils import FilterProductEngine
from core.mixins import MetaMixin
import json
from django.template import RequestContext
from pdf_pages.mixins import PDFPageMixin


class MainPage(PDFPageMixin, MetaMixin, ListView):
    model = Product
    queryset = Product.objects.with_variants()
    context_object_name = 'products'
    template_name = 'catalog/main_page.html'
    paginate_by = 20
    paginate_orphans = 10

    def get_queryset(self, page=1):
        queryset = super(MainPage, self).get_queryset()
        sorting = self.request.session.get('sorting', None) or\
            ProductSorting.objects.order_by('-position').first()
        filters = self.request.GET.copy()
        filter_engine = FilterProductEngine()
        products = filter_engine.filter_products(queryset, filters, sorting)
        return products

    def post(self, request):
        self.kwargs.update({'page': request.POST.get('page', 1)})
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        html = render_to_string(
            'catalog/products.html', RequestContext(request, {
                'products': context['products'],
            })
        )
        if context['page_obj'].has_next():
            next_page = context['page_obj'].next_page_number()
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

