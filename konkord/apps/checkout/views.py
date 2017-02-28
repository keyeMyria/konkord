from django.views.generic import (
    DetailView, FormView, ListView, View)
from django.http import JsonResponse
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.shortcuts import get_object_or_404

import json

from catalog.models import Product
from delivery.models import City
from core.mixins import MetaMixin
from pdf_pages.mixins import PDFPageMixin

from .models import (
    CartItem, Order, PaymentMethod, ShippingMethod
)
from .forms import CheckoutForm
from .processors import BasePaymentProcessor
from .mixins import CheckoutMixin
from .utils import get_voucher_data_for_user


class JSONResponseMixin(object):
    http_method_names = ['post']

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        return context

    def post(self, request, *args, **kwargs):
        return self.render_to_response(kwargs)

    @staticmethod
    def bad_response_data(response_message=''):
        return {
            'status': 400,
            'message': 'Bad request',
            'data': {
                'message': response_message
            }
        }


class CheckoutView(MetaMixin, CheckoutMixin, FormView):
    form_class = CheckoutForm

    template_name = 'checkout/checkout.html'

    def dispatch(self, request, *args, **kwargs):
        self.voucher = self.request.POST.get(
            'voucher', self.request.session.get('voucher'))
        if self.voucher:
            self.voucher_data = get_voucher_data_for_user(
                self.request, self.voucher)
        return super(CheckoutView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['cart'] = self.get_cart()
        if context['cart']:
            context['total_price'] = context['cart'].get_total_price()
            if self.voucher:
                context['voucher_data'] = self.voucher_data
                context['total_price'] -= self.voucher_data.get('discount', 0)

        return context

    def form_valid(self, form):
        if self.voucher and not self.voucher_data['voucher_effective']:
            return self.form_invalid(form)
        return self.process_payment(form)

    def process_payment(self, form):
        # payment_method = form.cleaned_data['payment_method']
        # TODO replace it with payment method processor
        return BasePaymentProcessor(
            self.request, self.get_cart(), form).process()

    def get_breadcrumbs(self):
        return [(_('Checkout'), reverse('checkout'))]


class BuyProductsView(JSONResponseMixin, CheckoutMixin, View):

    @transaction.atomic
    def get_data(self, context):
        products_data = json.loads(self.request.POST.get('products', '[]'))
        cart = self.get_cart(create=True)
        try:
            products_dict = {
                int(product_id): amount for product_id, amount in products_data}
            products = Product.objects.filter(id__in=products_dict.keys())
            for product in products:
                amount = products_dict[product.id]
                if int(amount) <= 0:
                    continue
                if not product.status.show_buy_button:
                    return self.bad_response_data(
                        _(f'Product {product.name} cant be bought'))
                cart_item, created = CartItem.objects.get_or_create(
                    product_id=int(product.id),
                    cart=cart
                )
                cart_item.amount += int(amount)
                cart_item.save()
        except TypeError:
            return self.bad_response_data()
        except ValueError:
            return self.bad_response_data()
        if not cart.items.exists():
            return self.bad_response_data()
        return {
            'status': 200,
            'message': 'ok',
            'data': {
                'total_in_cart': cart.get_total_amount(),
                'total_cart_price': cart.get_total_price()
            }
        }


class UpdateCartView(JSONResponseMixin, CheckoutMixin, View):
    def get_data(self, context):
        update_data = json.loads(self.request.POST.get('update_data'))
        data_to_update = {}
        try:
            for cart_item_id, amount in update_data:
                data_to_update[int(cart_item_id)] = int(amount)
        except TypeError:
            return self.bad_response_data()
        except ValueError:
            return self.bad_response_data()
        items_data = {}
        for item in CartItem.objects.filter(id__in=data_to_update.keys()):
            item.amount = data_to_update[item.id]\
                if data_to_update[item.id] > 0 else 0
            items_data[item.id] = item.amount
            if not item.amount:
                item.delete()
            else:
                item.save()
        cart = self.get_cart()
        return {
            'status': 200,
            'message': 'ok',
            'data': {
                'total_in_cart': cart.get_total_amount(),
                'total_cart_price': cart.get_total_price(),
                'items': items_data
            }
        }


class DeleteCartItemsView(JSONResponseMixin, CheckoutMixin, View):
    def get_data(self, context):
        cart = self.get_cart()
        data = {}
        if cart:
            ids = json.loads(self.request.POST.get('items', '[]'))
            cart.items.filter(id__in=ids).delete()
            data = {
                'total_in_cart': cart.get_total_amount(),
                'total_cart_price': cart.get_total_price()
            }
        return {
            'status': 200,
            'message': 'ok',
            'data': data
        }


class CartDetailView(MetaMixin, CheckoutMixin, DetailView):

    template_name = 'checkout/cart/detail.html'

    def get_object(self, **kwargs):
        return self.get_cart()

    def get_context_data(self, **kwargs):
        context = super(CartDetailView, self).get_context_data(**kwargs)
        if context.get('cart'):
            context['total_price'] = context['cart'].get_total_price()
        return context


class CartDetailJSONView(JSONResponseMixin, CheckoutMixin, View):
    template_name = 'checkout/cart/detail.html'

    def get_data(self, context):
        cart = self.get_cart()
        if cart is None:
            return self.bad_response_data()
        data = {
            'total_in_cart': cart.get_total_amount(),
            'cart_price': cart.get_total_price()
        }
        return {
            'status': 200,
            'message': 'ok',
            'data': data
        }


@method_decorator(login_required, name='dispatch')
class OrderListView(MetaMixin, ListView):
    model = Order
    queryset = Order.objects.all()
    template_name = 'checkout/order/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.request.user.orders.order_by('-created')

    def get_breadcrumbs(self):
        return [
            (_('Account'), None),
            (_('My orders'), None)
        ]


@method_decorator(login_required, name="dispatch")
class OrderDetailView(PDFPageMixin, MetaMixin, DetailView):
    template_name = 'checkout/order/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Order, user=self.request.user, id=self.kwargs.get('order_id'))

    def get_breadcrumbs(self):
        obj = self.get_object()
        return [
            (_('Account'), None),
            (_('My orders'), reverse('order_list')),
            (_('Order # %s') % obj.get_number(), None)
        ]


class PaymentMethodDetail(JSONResponseMixin, View):

    def get_data(self, context):
        try:
            method = PaymentMethod.objects.get(
                id=self.request.POST.get('method', 0))
        except:
            return self.bad_response_data()

        return {
            'status': 200,
            'message': 'ok',
            'data': {
                'id': method.id,
                'price': method.get_price(**self.request.POST),
                'description': method.description
            }
        }


class ShippingMethodDetail(JSONResponseMixin, View):

    def get_data(self, context):

        try:
            method = ShippingMethod.objects.get(
                id=self.request.POST.get('method', 0))
        except:
            return self.bad_response_data()

        return {
            'status': 200,
            'message': 'ok',
            'data': {
                'id': method.id,
                'price': method.get_price(**self.request.POST),
                'description': method.description
            }
        }


class ThankYouPageView(PDFPageMixin, MetaMixin, DetailView):
    template_name = 'checkout/thank_you.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        try:
            order = Order.objects.get(
                Q(id=self.request.session.pop('order_id', None)) |
                Q(uuid=self.request.POST.get('order'))
            )
        except Order.DoesNotExist:
            order = None
        return order

    def get_breadcrumbs(self):
        return [(_('Than you'), None)]


class ShippingMethodCities(JSONResponseMixin, View):

    def get_data(self, context):
        try:
            method = ShippingMethod.objects.exclude(delivery_service=None).get(
                id=int(self.request.POST.get('method')))
            cities = method.delivery_service.service.cities.filter(
                active=True).values('id', 'name')
            return {
                'status': 200,
                'message': 'ok',
                'data': {
                    'cities': list(cities)
                }
            }
        except:
            return self.bad_response_data()


class ShippingMethodCityOffices(JSONResponseMixin, View):

    def get_data(self, context):
        try:
            city = City.objects.get(
                delivery_service__deliveryservicerelation__shipping_method__id=
                self.request.POST.get('method'),
                id=self.request.POST.get('city'),
                active=True
            )
            return {
                'status': 200,
                'message': 'ok',
                'data': {
                    'offices': list(city.offices.filter(
                        active=True).values('id', 'address'))
                }
            }
        except:
            return self.bad_response_data()


class VoucherJSONView(JSONResponseMixin, View):

    def get_data(self, context):
        try:
            voucher_data = get_voucher_data_for_user(self.request)
            voucher_data.pop('voucher', None)
            return {
                'status': 200,
                'message': 'ok',
                'data': voucher_data
            }
        except:
            return self.bad_response_data()