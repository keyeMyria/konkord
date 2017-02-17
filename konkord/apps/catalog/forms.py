from core.utils import check_pattern_exist
from django import forms
from .models import Product
from django.utils.translation import ugettext_lazy as _
from seo.forms import SeoFormMixin


class ProductForm(SeoFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = SeoFormMixin.Meta.widgets

    def clean_slug(self):
        data = self.cleaned_data['slug']
        if check_pattern_exist(data, self.instance):
            raise forms.ValidationError(
                _(
                    u'%s already used as slug for another object '
                    u'or as url pattern') % data)
        return data
