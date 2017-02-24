# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from adminconfig.utils import BaseConfig


class CheckoutJobsConfigForm(forms.Form):
    send_mail_after = forms.CharField(
        label=_(u'Send mail after'),
        help_text=_(u'Time, in minutes, separated by commas'))


class CheckoutJobsConfig(BaseConfig):
    form_class = CheckoutJobsConfigForm
    block_name = 'checkout_jobs'
    name = _('Checkout jobs')
    default_data = {
        'CART_CHANGED_EMAIL_SEND_AFTER': '3',

    }

    option_translation_table = (
        ('CART_CHANGED_EMAIL_SEND_AFTER', 'send_mail_after')

    )

