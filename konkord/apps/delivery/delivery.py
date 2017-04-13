# -*- coding: utf-8 -*-


def update_delivery():
    from delivery.models import (
        City, DeliveryService, DeliveryOffice
    )
    from pytils.translit import slugify
    import requests
    import json
    delivery_service = DeliveryService.objects.get_or_create(
        update_source='delivery', defaults={'name': 'Delivery'})[0]
    api_url = 'http://www.delivery-auto.com/api/'
    url_cities = "Public/GetAreasList?culture=ru-RU"
    url_warehousesList = "Public/GetWarehousesList?culture=ru-RU&includeRegionalCenters=true&CityId={CityId}"
    url_warehouseInfo = "Public/GetWarehousesInfo?culture=ru-RU&WarehousesId={WarehousesId}"
    req_cities = requests.get(api_url + url_cities)
    cities = json.loads(req_cities.content)['data']
    cities_data = {}
    warehouses_data = {}
    all_cities = {}
    for city in cities:
        if city['IsWarehouse']:
            if 'warehouses' not in city:
                city['warehouses'] = []
            warehouse_list = json.loads(
                requests.get(api_url + url_warehousesList.format(
                    CityId=city['id']
                )).content)['data']
            for warehouse in warehouse_list:
                city['warehouses'].append(json.loads(
                    requests.get(api_url + url_warehouseInfo.format(
                        WarehousesId=warehouse['id']
                    )).content)['data'])
            warehouses = city.pop('warehouses')
            cities_data[city['id']] = city
            for warehouse in warehouses:
                warehouses_data[warehouse['id']] = warehouse

    exist_cities = City.objects.filter(
        delivery_service=delivery_service, identificator__in=cities_data.keys())
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
            slug=slugify(city_data['name']),
            name=city_data['name'],
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
        office.city = all_cities[warehouses_data[office.identificator]['CityId']]
        office.phone = warehouses_data[office.identificator]['RcPhone']
        office.extra = warehouses_data[office.identificator]
        office.active = True
        office.save()
        warehouses_data.pop(office.identificator)
    DeliveryOffice.objects.bulk_create(
        DeliveryOffice(
            city=all_cities[warehouse_data['CityId']],
            identificator=warehouse_ref,
            name=warehouse_data['name'],
            address=warehouse_data['address'],
            phone=warehouse_data['RcPhone'],
            extra=warehouses_data,
            active=True
        )
        for warehouse_ref, warehouse_data in warehouses_data.items()
    )

    active_cities_ids = DeliveryOffice.objects.filter(
        active=True
    ).order_by('city').distinct('city').values_list('city', flat=True)
    City.objects.exclude(id__in=active_cities_ids).update(
        active=False)
    City.objects.filter(id__in=active_cities_ids).update(
        active=True)