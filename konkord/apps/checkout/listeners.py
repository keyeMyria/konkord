from django.contrib.auth import user_logged_in
from django.db.models.signals import post_save, pre_delete
from .models import Cart, CartItem
from datetime import timedelta, timezone
from django.conf import settings
task_manager = settings.ACTIVE_TASK_QUEUE


def merge_carts(sender, user, request, **kwargs):
    try:
        session_cart = Cart.objects.get(session=request.session.session_key)
        user_cart = Cart.objects.get_or_create(user=user)[0]
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


def cart_changed_listener(sender, instance, **kwargs):
    if not settings.CART_CHANGED_EMAIL_SEND_AFTER and\
            instance.user is not None:
        return
    for time in settings.CART_CHANGED_EMAIL_SEND_AFTER.split(','):
        pending_tasks = task_manager.get_pending_tasks(
            'checkout.jobs.forgotten_cart_send_email_job')
        email_jobs_exists = False
        for task_id in pending_tasks:
            task = task_manager.get_task_instance(task_id)
            if task.kwargs.get('run_after') == time:
                email_jobs_exists = True
                break
        if not email_jobs_exists:
            task_manager.schedule(
                'checkout.jobs.forgotten_cart_send_email_job',
                kwargs={
                    'cart_modification_date':
                    instance.updated.strftime(
                        "%Y-%m-%d %H:%M:%S"),
                    'cart_id': instance.id,
                    'run_after': time
                    },
                run_after=instance.updated.replace(
                    tzinfo=timezone.utc
                ).astimezone(tz=None) + timedelta(
                    minutes=int(time)
                )
            )
post_save.connect(cart_changed_listener, sender=Cart)


def cart_item_changed_listener(sender, instance, **kwargs):
    instance.cart.save()

post_save.connect(cart_item_changed_listener, sender=CartItem)
pre_delete.connect(cart_item_changed_listener, sender=CartItem)