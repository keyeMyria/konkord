# EXPORT
from collections import OrderedDict
from lfs.catalog.models import (
    Product, ProductStatus, Property, ProductPropertyValue
)
from django.contrib.auth.models import User

LANG = 'uk'

STANDARD_PRODUCT = 0
PRODUCT_WITH_VARIANTS = 1
VARIANT = 2

PROPERTIES_UK_TO_RU = OrderedDict({
    u'Антипрокольна устілка': u'Антипрокольная стелька',
    u'Тип взуття': u'Тип обуви',
    u'Додатково': u'Дополнительно',
    u'Розмірний ряд': u'Размерный ряд',
    u'Метод крепления': u'Метод крепления',
    u'Степень защиты': u'Степень защиты',
    u'Перфорация': u'Перфорация',
    u'Підошва': u'Подошва',
    u'Розмір': u'Размер',
    u'Подносок': u'Подносок',
    u'Пяточний ремень': u'Пяточний ремень',
    u'Колір': u'Цвет',
    u'Основні значення': u'Основные значения',
    u'Матеріал верху': u'Материал верха',
    u'NB!': u'NB!',
    u'Оптова ціна від': u'Оптовая цена от',
    u'Стать': u'Пол',
    u'Хутро': u'Мех',
    u'СабоТуфлиБотнки': u'СабоТуфлиБотнки',

})


STATUSES_UK_TO_RU = OrderedDict({
    u'Архів': u'Архив',
    u'Під замовлення': u'Под заказ',
    u'Очікується': u'Ожидается',
    u'В наявності': u'В наличии',
    u'Не в наявності': u'Нет в наличии',
})

properties = {}
parent_products = OrderedDict()
variants_products = OrderedDict()
users_data = []
products_not_in_another_lang = {}


def write_json(users_data, properties, parent_products, variants_products):
    import json
    json_data = {
        'users': users_data,
        'properties': properties,
        'products': {
            'parent': [
                {'sku': sku, 'data': data}
                for sku, data in parent_products.iteritems()
            ],
            'variants': [
                {'name': name, 'data': data}
                for name, data in variants_products.iteritems()
            ]
        }
    }
    with open('migration_data.json', 'w') as outfile:
        json.dump(json_data, outfile)


def get_json():
    import json
    with open('migration_data.json') as infile:
        json_data = json.load(infile)
    p_products = json_data['products']['parent']
    v_products = json_data['products']['variants']
    pp_data = {}
    pv_data = {}
    for p in p_products:
        pp_data[p['sku']] = p['data']
    for p in v_products:
        pv_data[p['name']] = p['data']
    return json_data['users'], json_data['properties'], pp_data, pv_data

if LANG == 'uk':
    users_data, properties, parent_products, variants_products = get_json()


def get_product_data(p):
    data = {
        'id': p.id,
        'name': p.name,
        'slug': p.slug,
        'active': p.active,
        'categories': [category.name for category in p.categories.all()],
        'status_name': p.status.name,
        'manufacturer': p.manufacturer.name,
        'short_description': p.short_description,
        'description': p.description,
        'price': p.price,
        'parent': p.parent.sku if p.parent else None,
        'images': [
            {
                'url': image.image.url,
                'title': image.title,
                'position': image.position
            }
            for image in p.images.order_by('position')
        ],
        'ppvs': {}
    }
    for ppv in p.property_values.all():
        data['ppvs'][ppv.property.name] = {
            'property_name': ppv.property.name,
            'property_id': ppv.property_id,
            'value': ppv.value
        }
    return data


for prop in Property.objects.all():
    if LANG == 'ru':
        ru_name = prop.name
        properties[ru_name] = {
            'ru': {},
            'uk': {}
        }
    else:
        ru_name = PROPERTIES_UK_TO_RU[prop.name]
    properties[ru_name][LANG] = {
        'id': prop.id,
        'name': prop.name,
        'is_group': prop.is_group,
        'identificator': prop.identificator,
        'uid': prop.uid,
    }


for product in Product.objects.filter(
        sub_type=PRODUCT_WITH_VARIANTS).order_by('recommended_position'):
    product_data = get_product_data(product)
    if LANG == 'ru':
        parent_products[product.sku] = {
            'ru': {},
            'uk': {},
        }
    try:
        parent_products[product.sku][LANG] = product_data
    except KeyError:
        products_not_in_another_lang[product.sku] = product_data


for product in Product.objects.filter(
        sub_type=VARIANT).order_by('recommended_position'):
    product_data = get_product_data(product)
    if LANG == 'ru':
        variants_products[product.name] = {
            'ru': {},
            'uk': {},
        }
    try:
        variants_products[product.name][LANG] = product_data
    except KeyError:
        products_not_in_another_lang[product.name] = product_data

from django.contrib.auth.models import User
users = User.objects.all()
for user in users:
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'password': user.password,
        'username': user.username,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'emails': set([user.email]),
        'phones': set([]),
    }
    for customer in user.customer_set.all():
        for email in customer.emails.all():
            data['emails'].add(email.email)
        for phone in customer.phones.all():
            data['phones'].add(phone.number)
    data['emails'] = list(data['emails'])
    data['phones'] = list(data['phones'])
    users_data.append(data)
write_json(users_data, properties, parent_products, variants_products)

# IMPORT
from catalog.models import (
    Product, Property, ProductPropertyValue, Image, ProductStatus
)
from users.models import User, Email, Phone
from django.contrib.sites.models import Site
from django.contrib.redirects.models import Redirect
from pytils.translit import slugify
from django.core.files import File
from catalog.settings import VARIANT, PRODUCT_WITH_VARIANTS
import urllib
from _collections import OrderedDict


Product.objects.all().delete()
Property.objects.all().delete()
ProductStatus.objects.all().delete()
User.objects.all().delete()
Image.objects.all().delete()
Redirect.objects.all().delete()

site = Site.objects.get_current()

PROPERTIES_UK_TO_RU = OrderedDict({
    u'Антипрокольна устілка': u'Антипрокольная стелька',
    u'Тип взуття': u'Тип обуви',
    u'Додатково': u'Дополнительно',
    u'Розмірний ряд': u'Размерный ряд',
    u'Метод крепления': u'Метод крепления',
    u'Степень защиты': u'Степень защиты',
    u'Перфорация': u'Перфорация',
    u'Підошва': u'Подошва',
    u'Розмір': u'Размер',
    u'Подносок': u'Подносок',
    u'Пяточний ремень': u'Пяточний ремень',
    u'Колір': u'Цвет',
    u'Основні значення': u'Основные значения',
    u'Матеріал верху': u'Материал верха',
    u'NB!': u'NB!',
    u'Оптова ціна від': u'Оптовая цена от',
    u'Стать': u'Пол',
    u'Хутро': u'Мех',
    u'СабоТуфлиБотнки': u'СабоТуфлиБотнки',

})

HOST = 'https://yas-poltava.com'


STATUSES = {
    'Архив': ProductStatus.objects.get_or_create(
        name='Архив',
        show_buy_button=False,
        is_visible=False,
        in_search=False
    )[0],
    'Под заказ': ProductStatus.objects.get_or_create(
        name='Под заказ',
        show_buy_button=False,
        is_visible=False,
        in_search=False
    )[0],
    'Ожидается': ProductStatus.objects.get_or_create(
        name='Ожидается',
        show_buy_button=False,
        is_visible=False,
        in_search=False
    )[0],
    'В наличии': ProductStatus.objects.get_or_create(
        name='В наличии',
        show_buy_button=True,
        is_visible=True,
        in_search=True
    )[0],
    'Нет в наличии': ProductStatus.objects.get_or_create(
        name='Нет в наличии',
        show_buy_button=False,
        is_visible=False,
        in_search=False
    )[0],
}


def get_json():
    import json
    with open('migration_data.json') as infile:
        json_data = json.load(infile)
    p_products = json_data['products']['parent']
    v_products = json_data['products']['variants']
    pp_data = {}
    pv_data = {}
    for p in p_products:
        pp_data[p['sku']] = p['data']
    for p in v_products:
        pv_data[p['name']] = p['data']
    return json_data['users'], json_data['properties'], pp_data, pv_data

users_data, properties, parent_products, variants_products = get_json()

Property.objects.bulk_create(
    Property(
        name_ru=name,
        name_uk=data['uk']['name'],
        slug=data['ru']['identificator']
    ) for name, data in properties.items() if not data['ru']['is_group']
)
Property.objects.create(
    name_ru='Категория',
    name_uk='Категорія',
    slug=slugify('Категория')
)
Property.objects.create(
    name_ru='Производитель',
    name_uk='Виробник',
    slug=slugify('Производитель')
)
used_emails = set()
used_phones = set()
unique_users = {}
for user in users_data:
    user_emails = set(user['emails']).difference(used_emails)
    used_emails.update(used_emails)
    user_phones = set(user['phones']).difference(used_phones)
    used_phones.update(user_phones)
    if user['username'] in unique_users:
        print(f'User with username {user["username"]}, merged')
        emails = unique_users[user['username']]['emails']
        emails.update(user['emails'])
        unique_users[user['username']]['emails'] = emails
        phones = unique_users[user['username']]['phones']
        phones.update(user_phones)
        unique_users[user['username']]['phones'] = phones
        if not unique_users[user['username']]['first_name']:
            unique_users[user['username']]['first_name'] = user['first_name']
        if not unique_users[user['username']]['last_name']:
            unique_users[user['username']]['first_name'] = user['last_name']
    else:
        unique_users[user['username']] = {
            'password': user['password'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'is_active': user['is_active'],
            'is_staff': user['is_staff'],
            'is_superuser': user['is_superuser'],
            'emails': user_emails,
            'phones': user_phones,
        }
User.objects.bulk_create(
    User(
        username=username,
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        is_active=data['is_active'],
        is_staff=data['is_staff'],
        is_superuser=data['is_superuser'],
    ) for username, data in unique_users.items()
)
emails_create_list = []
phones_create_list = []
for username, data in unique_users.items():
    user_obj = User.objects.get(username=username)
    for email in data['emails']:
        emails_create_list.append(Email(user=user_obj, email=email))
    for phone in data['phones']:
        phones_create_list.append(Phone(user=user_obj, number=phone))
Email.objects.bulk_create(emails_create_list)
Phone.objects.bulk_create(phones_create_list)

pp_create_list = []
position = 0
for sku, data in parent_products.items():
    if not data['uk'].get('name'):
        print(f'sku: {sku} had no UK version')
    pp_create_list.append(
        Product(
            status=STATUSES[data['ru']['status_name']],
            name_ru=data['ru']['name'],
            name_uk=data['uk'].get('name'),
            slug=data['ru']['slug'],
            product_type=PRODUCT_WITH_VARIANTS,
            active=data['ru']['active'],
            sku=sku,
            position=position,
            short_description_ru=data['ru']['short_description'],
            short_description_uk=data['uk'].get('short_description'),
            full_description_ru=data['ru']['description'],
            full_description_uk=data['uk'].get('description'),
            price=data['ru']['price']
        )
    )
    if data['uk'].get('slug'):
        Redirect.objects.create(
            site=site, old_path=data['uk']['slug'], new_path=data['ru']['slug'])
    position += 1
Product.objects.bulk_create(pp_create_list)

ppvs_create_list = []

for p in Product.objects.filter(sku__in=parent_products.keys()):
    for p_name, ppv in parent_products[p.sku]['uk'].get('ppvs', {}).items():
        ru_ppv = parent_products[p.sku]['ru']['ppvs'][PROPERTIES_UK_TO_RU[p_name]]
        try:
            prop = Property.objects.get(name_ru=PROPERTIES_UK_TO_RU[p_name])
        except Property.DoesNotExist:
            print('prop', p_name)
            continue
        ppvs_create_list.append(
            ProductPropertyValue(
                product=p,
                property=prop,
                value_ru=ru_ppv['value'],
                value_uk=ppv['value'],
                slug_value=slugify(ru_ppv['value']),
            )
        )
    prop = Property.objects.get(name_ru='Категория')
    ppvs_create_list.append(
        ProductPropertyValue(
            product=p,
            property=prop,
            value_ru=','.join(parent_products[p.sku]['ru']['categories']),
            value_uk=','.join(parent_products[p.sku]['uk'].get(
                'categories', [])),
            slug_value=slugify(
                ','.join(parent_products[p.sku]['ru']['categories'])),
        )
    )
    prop = Property.objects.get(name_ru='Производитель')
    ppvs_create_list.append(
        ProductPropertyValue(
            product=p,
            property=prop,
            value_ru=parent_products[p.sku]['ru']['manufacturer'],
            value_uk=parent_products[p.sku]['uk'].get('manufacturer'),
            slug_value=slugify(parent_products[p.sku]['ru']['manufacturer']),
        )
    )
    for image in parent_products[p.sku]['ru']['images']:
        print(image)
        url = HOST + image['url']
        img_content = urllib.request.urlretrieve(url)
        product_image = Image(title=image['title'], product=p)
        product_image.position = image.get('position', 0)
        product_image.image.save(
            image['url'].split('/')[-1],
            File(open(img_content[0], 'rb')),
            save=True
        )
        product_image.save()

ProductPropertyValue.objects.bulk_create(ppvs_create_list)


pv_create_list = []
position = 0
for name, data in variants_products.items():
    if not data['uk'].get('name'):
        print(f'{name} had no UK version')
    pv_create_list.append(
        Product(
            status=ProductStatus.objects.get(name=data['ru']['status_name']),
            name_ru=data['ru']['name'],
            name_uk=data['uk'].get('name'),
            slug=data['ru']['slug'],
            parent=Product.objects.get(sku=data['ru']['parent']),
            product_type=VARIANT,
            active=data['ru']['active'],
            position=position,
            short_description_ru=data['ru']['short_description'],
            short_description_uk=data['uk'].get('short_description'),
            full_description_ru=data['ru']['description'],
            full_description_uk=data['uk'].get('description'),
            price=data['ru']['price']
        )
    )
    if data['uk'].get('slug'):
        Redirect.objects.create(
            site=site, old_path=data['uk']['slug'], new_path=data['ru']['slug'])
    position += 1
Product.objects.bulk_create(pv_create_list)

ppvs_create_list = []

for p in Product.objects.filter(name_ru__in=variants_products.keys()):
    for p_name, ppv in variants_products[p.name_ru]['uk'].get('ppvs', {}).items():
        try:
            ru_ppv = variants_products[p.name_ru]['ru']['ppvs'][PROPERTIES_UK_TO_RU[p_name]]
        except KeyError:
            print(variants_products[p.name_ru]['ru']['ppvs'].keys())
            print(p_name)
            continue
        try:
            prop = Property.objects.get(name_ru=PROPERTIES_UK_TO_RU[p_name])
        except Property.DoesNotExist:
            print('prop', p_name)
            continue
        ppvs_create_list.append(
            ProductPropertyValue(
                product=p,
                property=prop,
                value_ru=ru_ppv['value'],
                value_uk=ppv['value'],
                slug_value=slugify(ru_ppv['value']),
            )
        )
    prop = Property.objects.get(name_ru='Категория')
    ppvs_create_list.append(
        ProductPropertyValue(
            product=p,
            property=prop,
            value_ru=','.join(variants_products[p.name_ru]['ru']['categories']),
            value_uk=','.join(variants_products[p.name_ru]['uk'].get(
                'categories', [])),
            slug_value=slugify(
                ','.join(variants_products[p.name_ru]['ru']['categories'])),
        )
    )
    prop = Property.objects.get(name_ru='Производитель')
    ppvs_create_list.append(
        ProductPropertyValue(
            product=p,
            property=prop,
            value_ru=variants_products[p.name_ru]['ru']['manufacturer'],
            value_uk=variants_products[p.name_ru]['uk'].get('manufacturer'),
            slug_value=slugify(variants_products[p.name_ru]['ru']['manufacturer']),
        )
    )
    for image in variants_products[p.name]['ru']['images']:
        print(image)
        url = HOST + image['url']
        img_content = urllib.request.urlretrieve(url)
        product_image = Image(title=image['title'], product=p)
        product_image.position = image.get('position', 0)
        product_image.image.save(
            image['url'].split('/')[-1],
            File(open(img_content[0], 'rb')),
            save=True
        )
        product_image.save()

ProductPropertyValue.objects.bulk_create(ppvs_create_list)
