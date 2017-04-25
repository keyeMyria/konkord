"""
If you want use seo_data in your view, you need inherit your view from
seo.mixins.SeoMixin. Then you have three ways to set up seo data:
1. define get_object method at view, and this object must be inherited
    from seo.models.ModelWithSeoMixin
2. setup settings `ClassName_MetaParam_Language` in upper case. Also you
    can add this settings to configuration automaticly. You need to inherit
    your Config and ConfigForm classes from self.mixins.SeoConfigMixin and
    define `seo_config_prefixes` param, it must be list of names.
    Don't worry if you'll forget define it, in this case mixin will
    raise error
3. define meta attribute at view:
    meta_h1
    meta_title
    meta_keywords
    meta_description
    meta_seo_text
"""
