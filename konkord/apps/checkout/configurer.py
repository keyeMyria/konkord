# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from adminconfig.utils import BaseConfig
from seo.mixins import SeoConfigMixin


class CheckoutConfigForm(SeoConfigMixin, forms.Form):
    voucher_placeholder_ru = forms.CharField(
        label=_('Voucher placeholder ru'),
        required=False
    )
    voucher_placeholder_uk = forms.CharField(
        label=_('Voucher placeholder uk'),
        required=False
    )
    seo_config_prefixes = [
        'CheckoutView',
        'OrderListView',
        'OrderDetailView',
        'ThankYouPageView',
    ]


class CheckoutConfig(SeoConfigMixin, BaseConfig):
    form_class = CheckoutConfigForm
    block_name = 'checkout'
    name = _('Checkout')
    seo_config_prefixes = [
        'CheckoutView',
        'OrderListView',
        'OrderDetailView',
        'ThankYouPageView',
    ]
    default_data = {
        'CHECKOUT_VOUCHER_PLACEHOLDER_RU': 'Сертификат',
        'CHECKOUT_VOUCHER_PLACEHOLDER_UK': 'Сертифікат'
    }

    option_translation_table = (
        ('CHECKOUT_VOUCHER_PLACEHOLDER_RU', 'voucher_placeholder_ru'),
        ('CHECKOUT_VOUCHER_PLACEHOLDER_UK', 'voucher_placeholder_uk'),
    )


class CheckoutJobsConfigForm(forms.Form):
    send_mail_after = forms.CharField(
        label=_('Send mail after'),
        help_text=_('Time, in minutes, separated by commas'))


class CheckoutJobsConfig(BaseConfig):
    form_class = CheckoutJobsConfigForm
    block_name = 'checkout_jobs'
    name = _('Checkout jobs')
    default_data = {
        'CART_CHANGED_EMAIL_SEND_AFTER': '3',
    }

    option_translation_table = (
        ('CART_CHANGED_EMAIL_SEND_AFTER', 'send_mail_after'),
    )
