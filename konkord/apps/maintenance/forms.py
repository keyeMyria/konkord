from django import forms
from . import models
from suit_ckeditor.widgets import CKEditorWidget


class MaintenanceMessageForm(forms.ModelForm):
    class Meta:
        model = models.MaintenanceMessage
        widgets = {
            'message': CKEditorWidget
        }
        fields = '__all__'