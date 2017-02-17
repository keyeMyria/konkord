from modeltranslation.translator import translator, TranslationOptions
from .models import Product, Property, ProductPropertyValue, ProductStatus


class ProductTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'short_description',
        'full_description',
        'meta_title',
        'meta_h1',
        'meta_keywords',
        'meta_description',
        'meta_seo_text',
    )


translator.register(Product, ProductTranslationOptions)


class PropertyTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


translator.register(Property, PropertyTranslationOptions)


class ProductPropertyValueTranslationOptions(TranslationOptions):
    fields = (
        'value',
    )


translator.register(
    ProductPropertyValue, ProductPropertyValueTranslationOptions)


class ProductStatusTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


translator.register(ProductStatus, ProductStatusTranslationOptions)
