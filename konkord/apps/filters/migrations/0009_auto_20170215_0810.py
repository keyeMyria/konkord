# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0008_auto_20170131_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='properties',
            field=models.ManyToManyField(blank=True, related_name='filters', to='catalog.Property', verbose_name='Properties'),
        ),
    ]
