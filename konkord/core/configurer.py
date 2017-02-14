# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from adminconfig.utils import BaseConfig
from django.conf import settings
from django.utils.html import mark_safe


class CoreConfigForm(forms.Form):
    logo = forms.ImageField(label=_('Site logo'), required=False)

    def __init__(self, *args, **kwargs):
        super(CoreConfigForm, self).__init__(*args, **kwargs)
        logo = kwargs.get('initial', {}).get('logo', '')
        if logo and isinstance(logo, str):
            media_url = settings.MEDIA_URL
            self.fields['logo'].help_text = mark_safe(
                '<img src="%s"/ style="max-height: 40px;">' % (
                    media_url + logo.split(media_url)[-1])
            )


class CoreConfig(BaseConfig):
    form_class = CoreConfigForm
    block_name = 'core'
    default_data = {'SITE_LOGO': ''}
    option_translation_table = (
        ('SITE_LOGO', 'logo'),
    )
