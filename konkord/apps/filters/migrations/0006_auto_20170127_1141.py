# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 11:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0005_auto_20170127_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='type',
            field=models.CharField(choices=[('slider', 'Slider'), ('checkbox', 'Checkbox')], max_length=50, verbose_name='Type'),
        ),
    ]
