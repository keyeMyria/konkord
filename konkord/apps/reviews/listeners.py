from django.dispatch import receiver
from checkout.signals import order_created
from django.conf import settings
from datetime import datetime, timedelta
task_manager = settings.ACTIVE_TASK_QUEUE


@receiver(order_created)
def schedule_review_product_mail_job(**kwargs):
    now = datetime.now()
    task_manager.schedule(
        'reviews.jobs.review_product_mail_job',
        kwargs={'order_id': kwargs['order_id']},
        run_after=now + timedelta(
            minutes=settings.REVIEW_PRODCUT_MAIL_DELAY)
    )
