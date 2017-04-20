# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from adminconfig.utils import BaseConfig
from django.conf import settings
from django.utils.html import mark_safe
from .settings import WATERMARK_POSITION_CHOICES


class CoreConfigForm(forms.Form):
    logo = forms.ImageField(label=_('Site logo'), required=False)
    site_email = forms.EmailField(label=_('Site email'))
    shop_name_uk = forms.CharField(label=_('Shop name uk'))
    shop_name_ru = forms.CharField(label=_('Shop name ru'))
    shop_owner = forms.CharField(label=_('Shop owner'))
    default_currency = forms.CharField(label=_('Default currency'))
    currency_coefficient = forms.FloatField(label=_('Currency coefficient'))

    watermark = forms.ImageField(label=_('Watermark'), required=False)
    watermark_position = forms.ChoiceField(
        label=_('Watermark position'),
        choices=WATERMARK_POSITION_CHOICES
    )

    def __init__(self, *args, **kwargs):
        super(CoreConfigForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial', {})
        logo = initial.get('logo', {})
        watermark = initial.get('watermark', {})
        if logo:
            self.fields['logo'].help_text = mark_safe(
                '<img src="%s"/ style="max-height: 40px;">' % logo.get('url')
            )
        if watermark:
            self.fields['watermark'].help_text = mark_safe(
                '<img src="%s"/ style="max-height: 40px;">' % watermark.get(
                    'url')
            )

    def clean(self):
        cleaned_data = super(CoreConfigForm, self).clean()
        if not cleaned_data.get('watermark'):
            cleaned_data.pop('watermark', None)
        if not cleaned_data.get('logo'):
            cleaned_data.pop('logo', None)
        return cleaned_data


class CoreConfig(BaseConfig):
    form_class = CoreConfigForm
    block_name = 'core'
    name = _('Core')
    default_data = {
        'SITE_LOGO': {
            'url': settings.STATIC_URL + 'images/default_logo.png',
            'path': settings.STATIC_ROOT + 'images/default_logo.png'
        },
        'SITE_EMAIL': 'yaspoltava@gmail.com',
        'DEFAULT_CURRENCY': 'UAH',
        'SHOP_NAME_RU': '',
        'SHOP_NAME_UK': '',
        'WATERMARK:': {},
        'LEFT_WATERMARK_MARGIN': 0,
        'TOP_WATERMARK_MARGIN': 0,
        'WATERMARK_TRANSPARENCY': 0,
        'WATERMARK_POSITION': 1,
        'CURRENCY_COEFFICIENT': 1,
        'SHOP_OWNER': 'shop'
    }

    option_translation_table = (
        ('SITE_LOGO', 'logo'),
        ('SITE_EMAIL', 'site_email'),
        ('DEFAULT_CURRENCY', 'default_currency'),
        ('SHOP_NAME_RU', 'shop_name_ru'),
        ('SHOP_NAME_UK', 'shop_name_uk'),
        ('WATERMARK', 'watermark'),
        ('LEFT_WATERMARK_MARGIN', 'left_watermark_margin'),
        ('TOP_WATERMARK_MARGIN', 'top_watermark_margin'),
        ('WATERMARK_TRANSPARENCY', 'watermark_transparency'),
        ('WATERMARK_POSITION', 'watermark_position'),
        ('CURRENCY_COEFFICIENT', 'currency_coefficient'),
        ('SHOP_OWNER', 'shop_owner')
    )
