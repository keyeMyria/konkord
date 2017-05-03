# -*- coding: utf-8 -*-
from django.utils.translation import get_language
from django.conf import settings
from django import forms
from codemirror.widgets import CodeMirrorTextarea
from django.utils.translation import ugettext_lazy as _
from core.utils import render_meta_info


class SeoMixin(object):
    meta_h1 = None
    meta_title = None
    meta_keywords = None
    meta_description = None
    meta_seo_text = None

    def __init__(self, *args, **kwargs):
        super(SeoMixin, self).__init__(*args, **kwargs)
        lang = get_language()
        if lang:
            self._lang = lang.upper()
        self._class_name = self.__class__.__name__.upper()

    def get_context_data(self, **kwargs):
        context = super(SeoMixin, self).get_context_data(**kwargs)
        context.update({
            'h1': self.get_h1(),
            'meta_title': self.get_meta_title(),
            'meta_keywords': self.get_meta_keywords(),
            'meta_description': self.get_meta_description(),
            'meta_seo_text': self.get_meta_seo_text()
        })
        return context

    def _seo_context_data(self):
        context = {
            'shop_name': getattr(settings, f'SHOP_NAME_{self._lang}', ''),
            'request': self.request
        }
        return context

    def get_h1(self):
        settings_h1 = getattr(
            settings,
            f'{self._class_name}_META_H1_{self._lang}',
            None
        )
        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if hasattr(obj, 'get_h1'):
                return obj.get_h1(self.request)
        elif settings_h1 is not None:
            return render_meta_info(settings_h1, self._seo_context_data())
        elif self.meta_h1 is not None:
            return render_meta_info(self.meta_h1, self._seo_context_data())
        return ''

    def get_meta_title(self):
        settings_meta_title = getattr(
            settings,
            f'{self._class_name}_META_TITLE_{self._lang}',
            None
        )
        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if hasattr(obj, 'get_meta_title'):
                return obj.get_meta_title(self.request)
        elif settings_meta_title is not None:
            return render_meta_info(
                settings_meta_title, self._seo_context_data())
        elif self.meta_title is not None:
            return render_meta_info(self.meta_title, self._seo_context_data())
        return ''

    def get_meta_keywords(self):
        settings_meta_keywords = getattr(
            settings,
            f'{self._class_name}_META_KEYWORDS_{self._lang}',
            None
        )
        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if hasattr(obj, 'get_meta_keywords'):
                return obj.get_meta_keywords(self.request)
        elif settings_meta_keywords is not None:
            return render_meta_info(
                settings_meta_keywords, self._seo_context_data())
        elif self.meta_keywords is not None:
            return render_meta_info(
                self.meta_keywords, self._seo_context_data())
        return ''

    def get_meta_description(self):
        settings_meta_description = getattr(
            settings,
            f'{self._class_name}_META_DESCRIPTION_{self._lang}',
            None
        )
        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if hasattr(obj, 'get_meta_description'):
                return obj.get_meta_description(self.request)
        elif settings_meta_description is not None:
            return render_meta_info(
                settings_meta_description, self._seo_context_data())
        elif self.meta_description is not None:
            return render_meta_info(
                self.meta_description, self._seo_context_data())
        return ''

    def get_meta_seo_text(self):
        settings_meta_seo_text = getattr(
            settings,
            f'{self._class_name}_META_SEO_TEXT_{self._lang}',
            None
        )
        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if hasattr(obj, 'get_meta_seo_text'):
                return obj.get_meta_seo_text(self.request)
        elif settings_meta_seo_text is not None:
            return render_meta_info(
                settings_meta_seo_text, self._seo_context_data())
        elif self.meta_seo_text is not None:
            return render_meta_info(
                self.meta_seo_text, self._seo_context_data())
        return ''


class SeoConfigMixin(object):
    seo_config_prefixes = None
    seo_fields_list = [
        'meta_h1',
        'meta_title',
        'meta_keywords',
        'meta_description',
        'meta_seo_text'
    ]

    def __init__(self, *args, **kwargs):
        super(SeoConfigMixin, self).__init__(*args, **kwargs)
        if self.seo_config_prefixes is None:
            raise AttributeError(
                f'"seo_config_prefixes" must be defined for "{self.__class__}"'
            )
        if not isinstance(self.seo_config_prefixes, list):
            raise TypeError(
                f'"seo_config_prefixes" must be a list: {self.__class__}'
            )
        for prefix in self.seo_config_prefixes:
            for field_name in self.seo_fields_list:
                for code, name in settings.LANGUAGES:
                    if hasattr(self, 'fields'):
                        self.fields[f'{prefix.lower()}_{field_name}_{code}'] =\
                            forms.CharField(
                                label=_(f'{prefix} {field_name.replace("_", " ").title()} [{code}]'),
                                widget=CodeMirrorTextarea,
                                required=False
                        )
                    if hasattr(self, 'default_data'):
                        self.default_data[f'{prefix.upper()}_{field_name.upper()}_{code.upper()}'] =\
                        getattr(settings, f'{prefix.upper()}_{field_name.upper()}_{code.upper()}', None)
                    if hasattr(self, 'option_translation_table'):
                        self.option_translation_table += (
                            (
                                f'{prefix.upper()}_{field_name.upper()}_{code.upper()}',
                                f'{prefix.lower()}_{field_name}_{code}'
                            ),
                        )
