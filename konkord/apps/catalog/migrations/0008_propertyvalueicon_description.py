# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_propertyvalueicon'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyvalueicon',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]
