from price_navigator.models import PriceNavigator
from datetime import datetime, time, timedelta
from django.shortcuts import get_object_or_404
from django.template import Context, Template
from catalog.models import Product
from catalog.settings import PRODUCT_WITH_VARIANTS
from django.conf import settings
import zipfile
from django.contrib.sites.models import Site
import os
from django.utils.translation import activate

SHOP_PRICE_DIR = getattr(settings, 'SHOP_PRICE_DIR', settings.MEDIA_ROOT)
if not SHOP_PRICE_DIR.endswith('/'):
    SHOP_PRICE_DIR += '/'


def check_tasks(price_navigator, by_request=False):
    task_manager = settings.ACTIVE_TASK_QUEUE
    run_after = None
    if price_navigator.active:
        now = datetime.now()
        update_times = price_navigator.update_times.split(',')
        for update_time in price_navigator.update_times.split(','):
            update_time = datetime.combine(
                now, datetime.strptime(update_time.strip(' '), '%H:%M').time())
            if update_time > now:
                run_after = update_time
                break
        if not run_after:
            run_after = datetime.combine(
                now + timedelta(days=1),
                datetime.strptime(update_times[0].strip(' '), '%H:%M').time())

    if by_request:
        run_after = datetime.now()

    if run_after:
        task_manager.schedule(
            'price_navigator.utils.generate',
            kwargs={'price_navigator_id': price_navigator.id},
            run_after=run_after
        )


def generate(price_navigator_id):
    try:
        price_navigator = get_object_or_404(
            PriceNavigator,
            pk=price_navigator_id
        )

        products = Product.objects.filter(
            status__in=price_navigator.product_statuses.all()
        ).exclude(
            product_type=PRODUCT_WITH_VARIANTS
        )

        t = Template(price_navigator.template)
        c = Context({
            'date': '{:%Y-%m-%d %H:%M}'.format(datetime.now()),
            'products': products,
            'site': 'https://%s' % Site.objects.get_current()
        })

        if not os.path.exists(SHOP_PRICE_DIR):
            os.makedirs(SHOP_PRICE_DIR)
        for lang_code, lang_name in settings.LANGUAGES:
            path = SHOP_PRICE_DIR + lang_code + '_' + price_navigator.file_name
            activate(lang_code)
            text = t.render(c)
            for symbol in price_navigator.replacement:
                try:
                    replaceable = symbol.decode('string_escape').encode('utf8')
                except:
                    replaceable = symbol.decode('string_escape').decode('utf8')
                text = text.replace(
                    replaceable,
                    price_navigator.replacement[symbol].encode(
                        price_navigator.get_coding_display()
                    )
                )
            if price_navigator.pack_to_zip:
                zf = zipfile.ZipFile(path[:path.rfind('.')] + '.zip', mode='w')
                zf.writestr(price_navigator.file_name, text)
                zf.close()
            else:
                _file = open(
                    path,
                    'w',
                    encoding=price_navigator.get_coding_display())
                _file.write(text)
                _file.close()

            price_navigator.last_generation = datetime.now()
            price_navigator.save()
            check_tasks(price_navigator)
    except Exception as e:
        check_tasks(price_navigator)
        return str(e)
    return True
