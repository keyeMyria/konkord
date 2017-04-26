from django import forms
from datetime import datetime
from codemirror.widgets import CodeMirrorTextarea
from .models import PriceNavigator
from django.utils.html import mark_safe
from django.conf import settings
from .utils import SHOP_PRICE_DIR


class PriceNavigatorForm(forms.ModelForm):

    class Meta:
        model = PriceNavigator
        widgets = {
            'template': CodeMirrorTextarea(mode='xml', config={
                'fixedGutter': True,
                'lineWrapping': True,
            }),
        }
        exclude = []

    def __init__(self, *args, **kwargs):
        super(PriceNavigatorForm, self).__init__(*args, **kwargs)
        if self.instance:
            prices_url = settings.MEDIA_URL + SHOP_PRICE_DIR.split(
                '/media/')[-1]
            files_links = []
            for lang in settings.LANGUAGES:
                files_links.append(
                    '<a href="{lang_url}">{lang_name}</a>'.format(**{
                        'lang_url': '%s%s_%s' % (
                            prices_url, lang[0], self.instance.file_name),
                        'lang_name': lang[1]
                    })
                )
            file_name_help_text = mark_safe(' / '.join(files_links))
            self.fields['file_name'].help_text = file_name_help_text


    def clean_update_times(self):
        update_times = self.cleaned_data.get('update_times')
        if update_times:
            try:
                now = datetime.now()
                [datetime.combine(now, datetime.strptime(update_time.strip(
                    ' '), '%H:%M').time()) for update_time in update_times.split(',')]
            except:
                raise forms.ValidationError(_(u"Invalid data"))
        return update_times