# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from adminconfig.utils import BaseConfig
from django.conf import settings
from django.utils.html import mark_safe


class CoreConfigForm(forms.Form):
    logo = forms.ImageField(label=_('Site logo'), required=False)
    site_email = forms.EmailField(label=_('Site email'))
    default_currency = forms.IntegerField(label=_('Default currency'))

    def __init__(self, *args, **kwargs):
        super(CoreConfigForm, self).__init__(*args, **kwargs)
        logo = kwargs.get('initial', {}).get('logo', '')
        if logo and isinstance(logo, str):
            if settings.MEDIA_ROOT in settings.SITE_LOGO:
                logo_url = settings.MEDIA_URL + settings.SITE_LOGO.split(
                    settings.MEDIA_ROOT)[-1]
            else:
                logo_url = settings.SITE_LOGO
            self.fields['logo'].help_text = mark_safe(
                '<img src="%s"/ style="max-height: 40px;">' % logo_url
            )


class CoreConfig(BaseConfig):
    form_class = CoreConfigForm
    block_name = 'core'
    name = _('Core')
    default_data = {
        'SITE_LOGO': settings.STATIC_URL + 'images/default_logo.png',
        'SITE_EMAIL': 'yaspoltava@gmail.com',
        'DEFAULT_CURRENCY': 'UAH',
    }
    option_translation_table = (
        ('SITE_LOGO', 'logo'),
        ('SITE_EMAIL', 'site_email'),
        ('DEFAULT_CURRENCY', 'default_currency')
    )
