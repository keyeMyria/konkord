# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_propertyvalueicon_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='propertyvalueicon',
            options={'ordering': ('position',), 'verbose_name': 'Property value icon', 'verbose_name_plural': 'Property value icons'},
        ),
        migrations.AddField(
            model_name='propertyvalueicon',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='propertyvalueicon',
            name='description_uk',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='propertyvalueicon',
            name='title_ru',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Icon title'),
        ),
        migrations.AddField(
            model_name='propertyvalueicon',
            name='title_uk',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Icon title'),
        ),
    ]
