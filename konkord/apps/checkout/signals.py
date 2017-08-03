import django.dispatch


order_created = django.dispatch.Signal(providing_args=['order_id'])
