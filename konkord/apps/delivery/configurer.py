# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from adminconfig.utils import BaseConfig


class DeliveryConfigForm(forms.Form):
    nova_poshta_api_key = forms.CharField(
        label=_('Nova Poshta api key'), required=False)
    update_nova_poshta_cities = forms.BooleanField(
        label=_('Update Nova Poshta cities'), required=False)
    update_delivery_cities = forms.BooleanField(
        label=_('Update Delivery cities'), required=False
    )


class DeliveryConfig(BaseConfig):
    form_class = DeliveryConfigForm
    block_name = 'delivery'
    name = _('Delivery')
    default_data = {
        'NOVA_POSHTA_API_KEY': '',
        'DELIVERY_UPDATE_DELIVERY_CITIES': False,
        'DELIVERY_UPDATE_NOVA_POSHTA_CITIES': False
    }
    option_translation_table = (
        ('DELIVERY_NOVA_POSHTA_API_KEY', 'nova_poshta_api_key'),
        ('DELIVERY_UPDATE_DELIVERY_CITIES', 'update_delivery_cities'),
        ('DELIVERY_UPDATE_NOVA_POSHTA_CITIES', 'update_nova_poshta_cities'),
    )
