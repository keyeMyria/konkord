# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView
from django.template.loader import render_to_string
from django.http import HttpResponse
from catalog.models import Product, ProductSorting
from core.utils import FilterProductEngine
import json
from django.contrib.sites.models import Site
from django.template import RequestContext


class MainPage(ListView):
    model = Product
    queryset = Product.objects.active()
    context_object_name = 'products'
    template_name = 'catalog/main_page.html'
    paginate_by = 20
    paginate_orphans = 10

    def get_queryset(self, page=1):
        sorting = self.request.session.get('sorting', None) or\
            ProductSorting.objects.order_by('-position').first()
        filters = self.request.GET.copy()
        filter_engine = FilterProductEngine()
        products = filter_engine.filter_products(
            Product.objects.active(), filters, sorting)
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


class ProductView(DetailView):
    methods = ['GET']
    model = Product
    queryset = Product.objects.active()
    template_name = 'catalog/product_detail.html'
