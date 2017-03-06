from django import forms
from .models import PageCategory, Page
from suit_ckeditor.widgets import CKEditorWidget
from suit.widgets import LinkedSelect
from core.utils import check_pattern_exist
from django.utils.translation import ugettext_lazy as _
from seo.forms import SeoFormMixin


class PageCategoryForm(SeoFormMixin, forms.ModelForm):
    class Meta:
        model = PageCategory
        widgets = {
            'parent': LinkedSelect,
            'description': CKEditorWidget,
        }
        widgets.update(SeoFormMixin.Meta.widgets)
        exclude = []

    def clean_slug(self):
        data = self.cleaned_data['slug']
        if check_pattern_exist(data, self.instance):
            raise forms.ValidationError(
                _(
                    u'%s already used as slug for another object '
                    u'or as url pattern') % data)
        return data


class AddPageForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ('meta_title', 'meta_keywords', 'meta_description')
        widgets = {
            'preamble': CKEditorWidget,
            'text': CKEditorWidget,
            'type': forms.RadioSelect(),
        }


class EditPageForm(SeoFormMixin, forms.ModelForm):
    class Meta:
        model = Page
        widgets = {
            'preamble_ru': CKEditorWidget,
            'preamble_uk': CKEditorWidget,
            'text_ru': CKEditorWidget,
            'text_uk': CKEditorWidget,
            'type': forms.RadioSelect(),
        }
        widgets.update(SeoFormMixin.Meta.widgets)
        exclude = []
