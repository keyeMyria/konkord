# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View, DetailView
from django.core.paginator import QuerySetPaginator
from django.template.loader import render_to_string
from django.http import HttpResponse
from catalog.models import Product, ProductSorting
from core.utils import FilterProductEngine
from collections import deque
from itertools import count
import json


class MainPage(View):
    def define_page_range(self, current_page, total_pages, window=6):
        """ Returns range of pages that contains current page and few pages
        before and after it.

            @current_page - starts from 1
            @tota_pages - total number of pages
            @window - maximum number of pages shown with current page - should
            be even

            Examples (cucumber style):
                 Given window = 6
                 When current_page is 8
                 and total_pages = 20
                 Then I should see: 5 6 7 [8] 9 10 11

                 Given window = 6
                 When current_page is 8
                 and total_pages = 9
                 Then I should see: 3 4 5 6 7 [8] 9

                 Given window = 6
                 When current_page is 1
                 and total_pages = 9
                 Then I should see: [1] 2 3 4 5 6 7
        """
        # maximum length of page range is window + 1
        maxlen = window + 1
        page_range = deque(maxlen=maxlen)

        # minimum possible index is either: (current_page - window) or 1
        window_start = (current_page - window) \
            if (current_page - window) > 0 else 1

        # maximum possible index is current_page + window or total_pages
        window_end = total_pages if (current_page + window) > \
            total_pages else (current_page + window)

        # if we have enough pages then we should end at preffered end
        preffered_end = current_page + int(window / 2.0)

        for i in count(window_start):
            if i > window_end:
                # if we're on first page then our window will be [1] 2 3 4 5 6 7
                break
            elif i > preffered_end and len(page_range) == maxlen:
                # if we have enough pages already then stop at preffered_end
                break
            page_range.append(i)
        return list(page_range)

    def set_pagination_data(self, page_obj):
        """
        'page_range': page_range,
        'current_page': current_page_no,
        'total_pages': paginator.num_pages,
        'has_next': has_next,
        'has_prev': has_prev,
        'next': current_page_no + 1,
        'prev': current_page_no - 1,
        'url': url,
        'getparam': getparam,
        'first_page': first,
        'last_page': last,
        'getvars': '',
        'per_page': paginator.per_page,
        'formated_page_range': formated_page_range,
        'total_count': paginator.count
        """
        current_page = page_obj.number
        total_pages = self.paginator.num_pages
        page_range = self.define_page_range(current_page, total_pages)
        first_page = None if 1 in page_range else 1
        last_page = None if total_pages in page_range else total_pages
        self.pagination = {
            'has_prev': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'current_page': current_page,
            'total_pages': total_pages,
            'next': page_obj.number + 1,
            'prev': page_obj.number - 1,
            'first_page': first_page,
            'last_page': last_page,
            'per_page': self.paginator.per_page,
            'total_count': self.paginator.count,
            'getparam': 'page',
            'page_range': page_range
        }

    def get_products(self, page=1):
        sorting = self.request.session.get('sorting', None) or\
            ProductSorting.objects.order_by('-position').first()
        filters = self.request.GET.copy()
        filter_engine = FilterProductEngine()
        products = filter_engine.filter_products(
            Product.objects.active(), filters, sorting)
        self.paginator = QuerySetPaginator(products, 20)
        try:
            self.page_obj = self.paginator.page(page)
        except:
            self.page_obj = self.paginator.page(1)
        self.set_pagination_data(self.page_obj)
        return self.page_obj.object_list

    def get(self, request):
        self.request = request
        context = {
            'products': self.get_products(
                page=self.request.GET.get('page', 1)),
            'pagination': self.pagination
        }
        return render(request, 'catalog/main_page.html', context)

    def post(self, request):
        self.request = request
        html = render_to_string(
            'catalog/products.html', {'products': self.get_products(
                page=self.request.POST.get('page', 1))}
        )
        return HttpResponse(json.dumps({
            'products': html,
            'pagination': self.pagination
        }))


class ProductView(DetailView):
    methods = ['GET']
    model = Product
    queryset = Product.objects.active()
    template_name = 'catalog/product_detail.html'
