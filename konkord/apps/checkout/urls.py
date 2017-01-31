# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.CheckoutView.as_view(), name="checkout"),
    url(
        r'^buy-products$',
        views.BuyProductsView.as_view(),
        name="buy_products"
    ),
    url(
        r'^cart/update$',
        views.UpdateCartView.as_view(),
        name="update_cart"
    ),
    url(
        r'^cart/detail$',
        views.CartDetailView.as_view(),
        name="cart_detail"
    ),
    url(
        r'^cart/delete$',
        views.DeleteCartView.as_view(),
        name="cart_detail"
    ),
    url(
        r'^cart/delete-items$',
        views.DeleteCartItemsView.as_view(),
        name="cart_detail"
    ),
    url(
        r'^payment-method/detail',
        views.PaymentMethodDetail.as_view(),
        name="payment_method_detail"
    ),
    url(r'^order/list$', views.OrderListView.as_view(), name="order_list"),
    url(r'^order/detail', views.OrderDetailView.as_view(), name="order_detail"),
    url(r'^thank-you', views.ThankYouPageView.as_view(), name="thank_you_page")
]
