# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-11 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20170307_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='print_to_pdf',
            field=models.BooleanField(default=False, verbose_name='Print to pdf'),
        ),
    ]
