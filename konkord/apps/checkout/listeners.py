from django.contrib.auth import user_logged_in
from checkout.models import Cart


def merge_carts(sender, user, request, **kwargs):
    user_cart = Cart.objects.get_or_create(user=user)
    try:
        session_cart = Cart.objects.get(session=request.session.session_key)
        if user_cart.id != session_cart.id:
            for item in session_cart.items.all():
                item.cart = user_cart
                item.save()
            session_cart.delete()
            user_cart.session = request.session.session_key
            user_cart.save()
    except Cart.DoesNotExist:
        pass

user_logged_in.connect(merge_carts)
