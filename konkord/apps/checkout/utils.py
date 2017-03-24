# coding: utf-8
from .models import Cart, Voucher
from .settings import MESSAGES
import random

from .settings import (
    VOUCHER_LENGTH,
    VOUCHER_LETTERS,
    VOUCHER_PREFIX,
    VOUCHER_SUFFIX,
)


def create_voucher_number():
    number = ""
    for i in range(0, VOUCHER_LENGTH):
        number += random.choice(VOUCHER_LETTERS)

    return VOUCHER_PREFIX + number + VOUCHER_SUFFIX


def get_voucher_data_for_user(request, voucher_number=None):
    if not voucher_number:
        voucher_number = request.POST.get(
                'voucher', request.session.get('voucher'))
    try:
        cart = Cart.objects.get_user_cart(request)
    except Cart.DoesNotExist:
        return {
            'voucher_effective': False,
            'message': str(MESSAGES[6]),
            'voucher_number': voucher_number
        }
    cart_price = cart.get_total_price()
    try:
        voucher = Voucher.objects.get(number=voucher_number)
    except Voucher.DoesNotExist:
        if 'voucher' in request.POST and not request.POST['voucher']:
            request.session.pop('voucher', None)
        return {
            'voucher_effective': False,
            'message': str(MESSAGES[6]),
            'voucher_number': voucher_number
        }
    request.session['voucher'] = voucher.number
    voucher_effective, message = voucher.is_effective(cart_price)
    voucher_data = {
        'voucher_effective': voucher_effective,
        'message': message,
        'voucher': voucher,
        'voucher_name': voucher.name,
        'voucher_number': voucher_number,
        'voucher_type': voucher.type,
        'voucher_value': voucher.value 
    }
    if voucher_effective:
        voucher_data['discount'] = voucher.get_discount(cart_price)
    return voucher_data
