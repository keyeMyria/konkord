from .models import Cart
from django.db.models import Q
from django.db import transaction


class CheckoutMixin(object):
    @transaction.atomic
    def get_cart(self, create=False):
        try:
            cart = Cart.objects.get(
                Q(user=self.request.user)
                if self.request.user.is_authenticated() else
                Q(session=self.request.session.session_key)
            )
        except Cart.DoesNotExist:
            if create:
                data = {}
                if self.request.user.is_authenticated():
                    data['user'] = self.request.user
                else:
                    data['session'] = self.request.session.session_key
                cart = Cart.objects.create(**data)
            else:
                cart = None
        return cart
