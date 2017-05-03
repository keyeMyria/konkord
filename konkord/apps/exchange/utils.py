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
            product_id__in=products.values_list('id', flat=True)
        ).select_related('property')
        for ppv in all_ppvs:
            product_ppvs[ppv.product_id].append(ppv)
        prop_names_fields = [
            'property__name_%s' % lang[0] for lang in settings.LANGUAGES]
        properties = all_ppvs.values(
            'property__uuid', *prop_names_fields
        ).order_by('property_id').distinct('property_id')
        for prop in properties:
            xls_fields_map[prop['property__uuid']] = index
            props_name = '###'.join([
                prop[field_name] for field_name in prop_names_fields
            ])
            ws.write(0, index, props_name)
            ws.write(1, index, 'prop_' + str(prop['property__uuid']))
            index += 1
    parent_products = products.with_variants().values(*fields_to_export)
    variants = products.variants().values(*fields_to_export)
    variants_dict = defaultdict(list)
    for v in variants:
        variants_dict[v['parent_id']].append(v)
    row_num = 2

    def write_product(product, row_num):
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
                values = '###'.join([
                    getattr(ppv, 'value_%s' % lang[0], '') or ''
                    for lang in settings.LANGUAGES
                ])
                ws.write(row_num, col_num, values)
        return row_num + 1

    for product in parent_products:
        row_num = write_product(product, row_num)
        for variant in variants_dict.get(product['id'], []):
            row_num = write_product(variant, row_num)
    media_path = settings.MEDIA_ROOT
    file_name = '/products.xls'
    file_path = media_path + file_name
    ws.set_panes_frozen(True)
    ws.set_horz_split_pos(2)
    wb.save(file_path)
    return '/media' + file_name
