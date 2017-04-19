from core.utils import check_pattern_exist
from django import forms
from . import models
from dal import autocomplete, forward
from django.utils.translation import ugettext_lazy as _
from seo.forms import SeoFormMixin
from .settings import PRODUCT_WITH_VARIANTS, ANALOGOUS_PRODUCTS_TYPES
from core.widgets import ClearableImageInputWithThumb
from suit_ckeditor.widgets import CKEditorWidget


class ProductForm(SeoFormMixin, forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'
        widgets_dict = SeoFormMixin.Meta.widgets
        widgets_dict.update({
            'parent': autocomplete.ModelSelect2(
                url='product-autocomplete',
                forward=(
                    forward.Field('slug', 'exclude_slug'),
                    forward.Const([PRODUCT_WITH_VARIANTS], 'filter_sub_types'),
                )
            ),
            'short_description_ru': CKEditorWidget,
            'short_description_uk': CKEditorWidget,
            'full_description_ru': CKEditorWidget,
            'full_description_uk': CKEditorWidget,
        })
        widgets = widgets_dict

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


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Image
        fields = '__all__'
        widgets = {
            'image': ClearableImageInputWithThumb
        }