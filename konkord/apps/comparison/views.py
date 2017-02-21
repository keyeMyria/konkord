# coding: utf-8
from django.views.generic import TemplateView, ListView
from core.mixins import JSONResponseMixin
from catalog.models import Product, ProductPropertyValue
from _collections import defaultdict, OrderedDict
import json


class AddProductView(JSONResponseMixin, TemplateView):
    def get_data(self, context):
        request = self.request
        product_id = request.POST.get('product')
        try:
            Product.objects.active().get(pk=product_id)
        except Product.DoesNotExist:
            return self.bad_response_data()
        comparison_list = set(request.session.get('comparison', []))
        comparison_list.add(int(product_id))
        comparison_list = list(comparison_list)
        request.session['comparison'] = comparison_list
        data = {'comparison': list(comparison_list)}
        return self.success_response(data)


class RemoveProductsView(JSONResponseMixin, TemplateView):
    def get_data(self, context):
        request = self.request
        data = json.loads(request.POST.get('data', ''))
        clear = data.get('clear', False)
        comparison_list = set(request.session.get('comparison', []))
        if clear:
            comparison_list.clear()
        else:
            comparison_list = comparison_list.difference(
                set(data.get('products', [])))
        comparison_list = list(comparison_list)
        request.session['comparison'] = comparison_list
        data = {'comparison': list(comparison_list)}
        return self.success_response(data)


class ComparisonProductsView(JSONResponseMixin, TemplateView):
    def get_data(self, context):
        data = {'comparison': list(self.request.session.get('comparison', []))}
        return self.success_response(data)


class ComparisonView(ListView):

    template_name = 'comparison/comparison.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(
            id__in=self.request.session.get('comparison', []))

    def get_context_data(self, **kwargs):
        context = super(ComparisonView, self).get_context_data(**kwargs)
        products = context[self.context_object_name]
        products_properties = defaultdict(dict)
        groups_for_products = OrderedDict()
        ppvs = ProductPropertyValue.objects.filter(product__in=products)
        properties = set()
        for ppv in ppvs:
            products_properties[ppv.product_id][ppv.property.name] = ppv
            properties.add(ppv.property.name)
        for prop in properties:
            for product in products:
                if prop not in groups_for_products:
                    groups_for_products[prop] = OrderedDict()
                ppv = products_properties[product.id].get(prop)
                groups_for_products[prop][product.id] =\
                    ppv.value if ppv else None
        context['groups_for_products'] = groups_for_products
        return context
