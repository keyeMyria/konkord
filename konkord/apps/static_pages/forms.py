from django import forms
from .models import PageCategory, Page
from suit_ckeditor.widgets import CKEditorWidget
from suit.widgets import LinkedSelect
from codemirror.widgets import CodeMirrorTextarea
from core.utils import check_pattern_exist
from django.utils.translation import ugettext_lazy as _


class PageCategoryForm(forms.ModelForm):
    class Meta:
        model = PageCategory
        widgets = {
            'parent': LinkedSelect,
            'description': CKEditorWidget,
            'meta_title': CodeMirrorTextarea(mode='xml', config={
                'fixedGutter': True,
                'lineWrapping': True,
            }),
            'meta_keywords': CodeMirrorTextarea(mode='xml', config={
                'fixedGutter': True,
                'lineWrapping': True,
            }),
            'meta_description': CodeMirrorTextarea(mode='xml', config={
                'fixedGutter': True,
                'lineWrapping': True,
            }),
        }
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


class EditPageForm(forms.ModelForm):
    class Meta:
        model = Page
        widgets = {
            'preamble': CKEditorWidget,
            'text': CKEditorWidget,
            'type': forms.RadioSelect(),
            'meta_title': CodeMirrorTextarea(mode='xml', config={
                'fixedGutter': True,
                'lineWrapping': True,
            }),
            'meta_keywords': CodeMirrorTextarea(mode='xml', config={
                'fixedGutter': True,
                'lineWrapping': True,
            }),
            'meta_description': CodeMirrorTextarea(mode='xml', config={
                'fixedGutter': True,
                'lineWrapping': True,
            }),
        }
        exclude = []
