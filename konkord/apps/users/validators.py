# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import phonenumbers
from django import forms


def validate_phone(value):
    try:
        phone_obj = phonenumbers.parse(value, 'UA')
    except:
        raise forms.ValidationError(
            _(u'The string is not a valid phone number.'))
    phone_type = phonenumbers.number_type(phone_obj)
    if phone_type == 99:
        raise forms.ValidationError(
            _(u"Invalid phone number."))
    return f'{phone_obj.country_code}{phone_obj.national_number}'
