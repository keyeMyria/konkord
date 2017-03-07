from .models import Cart
from django.db import transaction
from django.utils.translation import get_language


class CheckoutMixin(object):
    @transaction.atomic
    def get_cart(self, create=False):
        try:
            cart = Cart.objects.get_user_cart(self.request)
        except Cart.DoesNotExist:
            if create:
                data = {
                    'language': get_language()
                }
                if self.request.user.is_authenticated():
                    data['user'] = self.request.user
                else:
                    data['session'] = self.request.session.session_key
                cart = Cart.objects.create(**data)
            else:
                cart = None
        return cart
