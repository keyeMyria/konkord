from django.utils.translation import ugettext_lazy as _
from django import forms
from suit.widgets import SuitSplitDateTimeWidget, EnclosedInput


class JobSchedulingForm(forms.Form):
    next_start = forms.SplitDateTimeField(
        label=_('Next start'),
        widget=SuitSplitDateTimeWidget)
    repeat = forms.IntegerField(
        label=_('Repeat'), widget=EnclosedInput(append='min'))
    timeout = forms.IntegerField(
        label=_('Timeout'), widget=EnclosedInput(append='min'))
