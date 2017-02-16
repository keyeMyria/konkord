from django import forms
from .models import StaticBlock
from suit_ckeditor.widgets import CKEditorWidget


class StaticBlockForm(forms.ModelForm):
    class Meta:
        model = StaticBlock
        fields = '__all__'
        widgets = {
            'content_ru': CKEditorWidget,
            'content_uk': CKEditorWidget,
        }
