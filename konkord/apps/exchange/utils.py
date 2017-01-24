import xlwt
from django.conf import settings
from catalog.models import ProductPropertyValue
from collections import defaultdict


def xls_do_import(import_id):
    from .models import ImportFromXls
    ImportFromXls.objects.get(id=import_id).do_import()


def export_products_to_xls(products):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Products')
    fields_to_export = []
    add_properties = False
    xls_fields_map = {}
    index = 0
    for field, field_name in settings.XLS_PRODUCT_FIELDS:
        if field == 'property':
            add_properties = True
            continue
        else:
            xls_fields_map[field] = index
            fields_to_export.append(field)

        ws.write(0, index, str(field_name))
        ws.write(1, index, field)
        index += 1

    product_ppvs = defaultdict(list)
    if add_properties:
        all_ppvs = ProductPropertyValue.objects.filter(
            product__in=products)
        for ppv in all_ppvs:
            product_ppvs[ppv.product.id].append(ppv)
        properties = all_ppvs.values(
            'property__name', 'property__uuid'
        ).order_by('property__id').distinct('property_id')
        for prop in properties:
            xls_fields_map[prop['property__uuid']] = index
            ws.write(0, index, prop['property__name'])
            ws.write(1, index, 'prop_' + str(prop['property__uuid']))
            index += 1

    products = products.values(*fields_to_export)
    row_num = 2
    for product in products:
        for field in fields_to_export:
            col_num = xls_fields_map[field]
            value = product[field]
            if field == 'product_type':
                value = settings.XLS_PRODUCT_TYPES_MAP[value]
            if value is None:
                value = ''
            ws.write(row_num, col_num, value)
        if add_properties:
            for ppv in product_ppvs[product['id']]:
                col_num = xls_fields_map[ppv.property.uuid]
                ws.write(row_num, col_num, ppv.value)
        row_num += 1
    media_path = settings.MEDIA_ROOT
    file_name = '/products.xls'
    file_path = media_path + file_name
    ws.set_panes_frozen(True)
    ws.set_horz_split_pos(2)
    wb.save(file_path)
    return '/media' + file_name
