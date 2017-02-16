from modeltranslation.translator import translator, TranslationOptions
from .models import PaymentMethod, ShippingMethod, OrderStatus


class PaymentMethodTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
    )


translator.register(PaymentMethod, PaymentMethodTranslationOptions)


class ShippingMethodTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description'
    )


translator.register(ShippingMethod, ShippingMethodTranslationOptions)


class OrderStatusTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


translator.register(OrderStatus, OrderStatusTranslationOptions)
