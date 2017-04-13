# -*- coding: utf-8 -*-
from django.conf import settings
import json


# NovaPoshta

def nv_api_request(modelName, calledMethod, methodProperties={}):
    '''Make a connaction to the NovaPoshta API v.2.0 and
    makes a method call. Returns a result like JSON.
    '''
    import http.client, urllib.request, urllib.parse, urllib.error, base64

    headers = {
        # Request headers
        'Content-Type': 'application/json',
    }

    params = urllib.parse.urlencode({
    })

    data = {
        'modelName': modelName,
        'calledMethod': calledMethod,
        'apiKey': settings.NOVA_POSHTA_API_KEY,
        'methodProperties': methodProperties,
    }

    conn = http.client.HTTPConnection('api.novaposhta.ua')
    conn.request(
        "POST",
        "/v2.0/json/AddressGeneral/getWarehouses?%s" % params,
        json.dumps(data),
        headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return json.loads(str(data, 'utf-8'))


def api_request_template(modelName, calledMethod, methodProperties={}):
    import requests

    '''
    request template:
    {
         "apiKey": "ключ API пользователя",
         "modelName": "[имя модели]",
         "calledMethod": "[имя вызываемого метода]",

        "methodProperties": {
         "[свойство1]": "...",
         "[свойство2]": "..."
         }
    }
    '''
    api_url = 'https://api.novaposhta.ua/v2.0/json/'
    data = {
        "apiKey": settings.NOVA_POSHTA_API_KEY,
        "modelName": modelName,
        "calledMethod": calledMethod,
        "methodProperties": methodProperties,
    }
    r = requests.post(api_url, data=json.dumps(data), verify=False)

    return r


def update_nova_poshta():
    from delivery.models import (
        City, DeliveryService, DeliveryOffice
    )
    from pytils.translit import slugify
    cities = json.loads(
        api_request_template('Address', 'getCities', {"Page": "1"}).text
    )
    delivery_service = DeliveryService.objects.get_or_create(
        update_source='novaposhta', defaults={'name': 'Nova Poshta'})[0]
    cities_data = {}
    warehouses_data = {}
    # data for quick get objects
    all_cities = {}
    for city in cities['data']:
        city_name = city['DescriptionRu']
        city_slug = slugify(city_name)
        cities_data[city['Ref']] = {
            'name': city_name,
            'name_ua': city['Description'],
            'slug': city_slug
        }

    warehouses = json.loads(api_request_template(
        'Address', 'getWarehouses', {'CityRef': ""}).text
                            )

    for warehouse in warehouses['data']:
        warehouses_data[warehouse['Ref']] = {
            'name': warehouse['DescriptionRu'],
            'address': warehouse['DescriptionRu'],
            'city': warehouse['CityRef'],
            'phone': warehouse['Phone'],
            'extra': {
                'longitude': warehouse['Longitude'],
                'latitude': warehouse['Latitude'],
                'number': warehouse['Number'],
            },
        }

    exist_cities = City.objects.filter(
        identificator__in=cities_data.keys(), delivery_service=delivery_service)
    for city in exist_cities:
        if city.name == cities_data[city.identificator]['name']:
            cities_data.pop(city.identificator)
            continue
        city.name = cities_data[city.identificator]['name']
        city.title = cities_data[city.identificator]['name']
        city.save(update_fields=['name', 'title'])
        cities_data.pop(city.identificator)

    created_cities = City.objects.bulk_create(
        City(
            delivery_service=delivery_service,
            title=city_data['name'],
            slug=city_data['slug'],
            name=city_data['name'],
            name_ua=city_data['name_ua'],
            identificator=city_key
        ) for city_key, city_data in cities_data.items()
    )
    for city in list(exist_cities) + created_cities:
        all_cities[city.identificator] = city

    DeliveryOffice.objects.filter(
        city__delivery_service=delivery_service
    ).exclude(identificator__in=warehouses_data.keys()).update(active=False)

    for office in DeliveryOffice.objects.filter(
            identificator__in=warehouses_data.keys(),
            city__delivery_service=delivery_service
    ):
        office.name = warehouses_data[office.identificator]['name']
        office.address = warehouses_data[office.identificator]['address']
        office.city = all_cities[warehouses_data[office.identificator]['city']]
        office.phone = warehouses_data[office.identificator]['phone']
        office.extra = warehouses_data[office.identificator]['extra']
        office.active = True
        office.save()
        warehouses_data.pop(office.identificator)
    DeliveryOffice.objects.bulk_create(
        DeliveryOffice(
            city=all_cities[warehouse_data['city']],
            identificator=warehouse_ref,
            name=warehouse_data['name'],
            address=warehouse_data['address'],
            phone=warehouse_data['phone'],
            extra=warehouse_data['extra'],
            active=True
        )
        for warehouse_ref, warehouse_data in warehouses_data.items()
        if warehouse_data['city']
    )

    active_cities_ids = DeliveryOffice.objects.filter(
        active=True
    ).order_by('city').distinct('city').values_list('city', flat=True)
    City.objects.exclude(id__in=active_cities_ids).update(
        active=False)
    City.objects.filter(id__in=active_cities_ids).update(
        active=True)
