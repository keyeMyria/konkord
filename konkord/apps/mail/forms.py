# coding: utf-8
from django import forms
from .models import (
    MailTemplate,
)
from codemirror.widgets import CodeMirrorTextarea


class MailTemplateForm(forms.ModelForm):
    class Meta:
        model = MailTemplate
        widgets = {
            'text_template': CodeMirrorTextarea(mode='jinja2', config={
                'fixedGutter': True,
                'lineWrapping': True,
            }),
            'html_template': CodeMirrorTextarea(mode='jinja2', config={
                'fixedGutter': True,
                'lineWrapping': True,
            }),
        }
        exclude = []
