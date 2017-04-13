# -*- coding: utf-8 -*-


class SeoMixin(object):
    def get_context_data(self, **kwargs):
        context = super(SeoMixin, self).get_context_data(**kwargs)
        context.update({
            'h1': self.get_h1(),
            'meta_title': self.get_meta_title(),
            'meta_keuwords': self.get_meta_keywords(),
            'meta_description': self.get_meta_description(),
            'meta_seo_text': self.get_meta_seo_text()
        })
        return context

    def get_h1(self):
        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if hasattr(obj, 'get_h1'):
                return obj.get_h1(self.request)
        return None

    def get_meta_title(self):
        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if hasattr(obj, 'get_meta_title'):
                return obj.get_meta_title(self.request)
        return None

    def get_meta_keywords(self):
        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if hasattr(obj, 'get_meta_keywords'):
                return obj.get_meta_keywords(self.request)
        return None

    def get_meta_description(self):
        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if hasattr(obj, 'get_meta_description'):
                return obj.get_meta_description(self.request)
        return None

    def get_meta_seo_text(self):
        if hasattr(self, 'get_object'):
            obj = self.get_object()
            if hasattr(obj, 'get_meta_seo_text'):
                return obj.get_meta_seo_text(self.request)
        return None
