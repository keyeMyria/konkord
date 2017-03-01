from core.utils import check_pattern_exist
from django import forms
from . import models
from dal import autocomplete, forward
from django.utils.translation import ugettext_lazy as _
from .settings import PRODUCT_WITH_VARIANTS, ANALOGOUS_PRODUCTS_TYPES


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'
        widgets = {
            'parent': autocomplete.ModelSelect2(
                url='product-autocomplete',
                forward=(
                    forward.Field('slug', 'exclude_slug'),
                    forward.Const([PRODUCT_WITH_VARIANTS], 'filter_sub_types'),
                )
            )
        }

    def clean_slug(self):
        data = self.cleaned_data['slug']
        if check_pattern_exist(data, self.instance):
            raise forms.ValidationError(
                _(
                    u'%s already used as slug for another object '
                    u'or as url pattern') % data)
        return data


class AnalogousProductsForm(forms.ModelForm):
    class Meta:
        model = models.AnalogousProducts
        fields = '__all__'
        widgets = {
            'analogous_product': autocomplete.ModelSelect2(
                url='product-autocomplete',
                forward=(
                    forward.Field('slug', 'exclude_slug'),
                    forward.Const(ANALOGOUS_PRODUCTS_TYPES, 'filter_sub_types')
                )
            )
        }