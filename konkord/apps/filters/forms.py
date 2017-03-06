from django import forms
from dal import autocomplete
from . import models


class FilterForm(forms.ModelForm):
    class Meta:
        models = models.Filter
        fields = '__all__'
        widgets = {
            'properties': autocomplete.ModelSelect2Multiple(
                url='property-autocomplete')
        }