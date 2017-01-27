# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0004_filteroption_products_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filteroption',
            name='products',
            field=models.ManyToManyField(editable=False, related_name='filter_options', to='catalog.Product', verbose_name='Products'),
        ),
    ]
