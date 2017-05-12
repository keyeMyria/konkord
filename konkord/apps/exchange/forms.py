from django import forms
from exchange.models import ImportFromXls
from codemirror.widgets import CodeMirrorTextarea


class ImportFromXlsForm(forms.ModelForm):
    class Meta:
        model = ImportFromXls
        fields = '__all__'
        widgets = {
            'log': CodeMirrorTextarea
        }