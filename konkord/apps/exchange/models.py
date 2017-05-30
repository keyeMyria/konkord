# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from core.fields import UnicodeJSONField
import xlrd
from catalog.models import Product, ProductStatus, Property, \
    ProductPropertyValue
from pytils.translit import slugify
from django.utils.translation import ugettext_lazy as _
from catalog.settings import VARIANT, PRODUCT_WITH_VARIANTS, STANDARD_PRODUCT
from collections import defaultdict
import traceback


class ImportFromXls(models.Model):

    xls_file = models.FileField(
        upload_to='import_from_xml',
        verbose_name=_(u'Excell file')
    )
    price = models.BooleanField(default=True, verbose_name=_(u'Price'))

    data_map = UnicodeJSONField(
        verbose_name=_('Data map'),
        blank=True,
        null=True,
        help_text=_('Use this for add shortcuts for export')
    )
    short_description = models.BooleanField(
        default=True,
        verbose_name=_(u'Short description')
    )
    full_description = models.BooleanField(
        default=True,
        verbose_name=_(u'Description')
    )
    properties = models.BooleanField(
        default=False,
        verbose_name=_(u'Properties')
    )
    log = models.TextField(
        verbose_name=_(u'Log'),
        blank=True,
        null=True,
        default='',
        help_text=_('Errors caused in import process')
    )

    class Meta:
        verbose_name = _(u'File for import')
        verbose_name_plural = _(u'Files for import')

    def __unicode__(self):
        return self.xls_file.name

    def get_converted_field_value(self, value):
        if self.data_map:
            return self.data_map.get(value, value)
        return value

    def do_import(self):
        try:
            rb = xlrd.open_workbook(self.xls_file.path)
            sheet = rb.sheet_by_index(0)
            self.log = ''
            row_with_names = sheet.row_values(0)
            row_with_identifiers = sheet.row_values(1)
            cols_to_fields_map = {
                col_num: col
                for col_num, col in enumerate(row_with_identifiers)
            }
            reversed_product_types = {
                type_str: type_value
                for type_value, type_str in
                settings.XLS_PRODUCT_TYPES_MAP.items()
            }
            id_col = None
            for col, field in cols_to_fields_map.items():
                if field == 'id':
                    id_col = col
                    break
            else:
                self.log = _('Id col missing')
                self.save()
                return
            properties = {}
            ppvs_to_create = []
            if self.properties:
                for col_num, col in enumerate(row_with_identifiers):
                    if cols_to_fields_map[col_num].startswith('prop_'):
                        property_uuid = cols_to_fields_map[col_num].split(
                            'prop_')[-1]
                        if not property_uuid:
                            index = 1
                            initial_slug = slugify(
                                row_with_names[col_num].split('###')[0])
                            slug = initial_slug
                            while Property.objects.filter(slug=slug).exists():
                                slug = f'{initial_slug}_{index}'
                                index += 1
                            prop_lang_names = \
                                row_with_names[col_num].split('###')
                            prop_names = {}
                            for lang_index, lang in enumerate(
                                    settings.LANGUAGES):
                                try:
                                    prop_names['name_%s' % lang[0]] = \
                                        prop_lang_names[lang_index]
                                except IndexError:
                                    pass
                            prop = Property.objects.create(
                                slug=slug, **prop_names)
                        else:
                            try:
                                prop = Property.objects.get(uuid=property_uuid)
                            except Property.DoesNotExist:
                                self.log += _(
                                    f'Property {row_with_names[col_num]} does not exist, ignored\n'
                                ).__str__()
                                continue
                        properties[col_num] = prop

            # get product_type field col_num
            product_type_col = None
            for col_num, col in enumerate(row_with_identifiers):
                if col == 'product_type':
                    product_type_col = col_num
                    break
            else:
                self.log = _('Product type col missing')
                self.save()
                return

            rows_for_ptypes = defaultdict(list)
            for rownum in range(2, sheet.nrows):
                row = sheet.row_values(rownum)
                ptype = reversed_product_types[row[product_type_col]]
                rows_for_ptypes[ptype].append(row)

            sorted_rows = []

            for ptype in [PRODUCT_WITH_VARIANTS, VARIANT, STANDARD_PRODUCT]:
                sorted_rows.extend(rows_for_ptypes[ptype])
            for row in sorted_rows:
                product_id = row[id_col]
                if product_id:
                    product_id = int(product_id)
                    try:
                        product = Product.objects.get(id=product_id)
                    except Product.DoesNotExist:
                        self.log += _(
                            f'Product with ID:({product_id}) does not exist\n'
                        ).__str__()
                        continue
                    except Product.MultipleObjectsReturned:
                        self.log += _(
                            f'Product with ID:({product_id}) repeats multiple times, skipped\n'
                        ).__str__()
                        continue
                else:
                    product = Product()
                ppvs = {}
                skip_product = False
                for col_num, col in enumerate(row):
                    field = cols_to_fields_map[col_num]
                    value = self.get_converted_field_value(col)
                    if field.startswith('name_'):
                        value = str(value).replace('.0', '')
                    if field == 'id':
                        continue
                    elif field == 'status__name_ru':
                        try:
                            status = ProductStatus.objects.get(name=value)
                        except ProductStatus.DoesNotExist:
                            self.log += _(
                                f'Product status {col} does not exist, product ID:({product_id}) skipped\n').__str__()
                            skip_product = True
                            break
                        product.status = status
                    elif field == 'product_type':
                        if value not in reversed_product_types:
                            self.log += _(
                                f'Invalid type {value} for product ID:({product_id}), product skipped\n').__str__()
                            skip_product = True
                            break
                        product.product_type = reversed_product_types[value]
                    elif field.startswith('prop_') and self.properties:
                        prop = properties.get(col_num)
                        if prop is None:
                            continue
                        ppvs[prop] = value
                    elif getattr(self, field, True):
                        if field == 'parent_id':
                            # parent_id is parent name
                            if value and isinstance(value, str):
                                try:
                                    product.parent_id = Product.objects.get(
                                        name=value).id
                                except Product.DoesNotExist:
                                    self.log += _(
                                        f'Parent product with Name:({value}) does not exist, product skipped\n'
                                    ).__str__()
                                    skip_product = True
                                    break
                                except Product.MultipleObjectsReturned:
                                    self.log += _(
                                        f'Parent product with Name:({value}) repeats multiple times, product skipped\n'
                                    ).__str__()
                                    skip_product = True
                                    break
                                continue
                        setattr(product, field, value)
                if skip_product:
                    continue
                if (product.product_type == VARIANT
                        and not product.parent_id) or\
                        (product.product_type in
                            [PRODUCT_WITH_VARIANTS, STANDARD_PRODUCT]
                            and product.parent_id):
                    self.log += _(
                        f'Invalid type for product ID:({product_id}), product skipped\n').__str__()
                    continue

                if not product.name:
                    self.log += _(
                        f'Product name must be set for ID:({product_id}), skipped\n').__str__()
                    continue
                if not product_id:
                    if Product.objects.filter(name=product.name).exists():
                        self.log += _(
                            f'Product with name {product.name} already exists, skipped\n').__str__()
                        continue
                    index = 1
                    initial_slug = slugify(product.name)
                    slug = initial_slug
                    while Product.objects.filter(slug=slug).exists():
                        slug = f'{initial_slug}_{index}'
                        index += 1
                    product.slug = slug
                    product.active = True
                product.save()
                if product_id:
                    ppvs_objects = ProductPropertyValue.objects.filter(
                        product_id=product.id, property__in=ppvs.keys()
                    ).select_related('property')
                    for ppv in ppvs_objects:
                        if not ppvs.get(ppv.property):
                            ppv.delete()
                            continue
                        ppv_lang_values = ppvs[ppv.property].split('###')
                        update_fields = []
                        for lang_index, lang in enumerate(settings.LANGUAGES):
                            lang_value_field = 'value_%s' % lang[0]
                            try:
                                lang_value = ppv_lang_values[lang_index]
                                if getattr(ppv, lang_value_field) != \
                                        lang_value:
                                    setattr(ppv, lang_value_field, lang_value)
                                    update_fields.append(lang_value_field)
                            except IndexError:
                                setattr(ppv, lang_value_field, '')
                                update_fields.append(lang_value_field)
                        ppv.save(update_fields=update_fields)
                        ppvs.pop(ppv.property)
                for prop, ppv in ppvs.items():
                    if ppv:
                        lang_values = {}
                        ppv_lang_values = ppvs[prop].split('###')
                        for lang_index, lang in enumerate(settings.LANGUAGES):
                            try:
                                lang_values['value_%s' % lang[0]] = \
                                    ppv_lang_values[lang_index]
                            except IndexError:
                                pass
                        ppvs_to_create.append(ProductPropertyValue(
                            product=product,
                            property=prop,
                            slug_value=slugify(str(ppv_lang_values[0])),
                            **lang_values
                        ))
            ProductPropertyValue.objects.bulk_create(ppvs_to_create)
        except:
            exc = traceback.format_exc()
            self.log = exc
        self.save()

