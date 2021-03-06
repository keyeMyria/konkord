# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0002_auto_20170126_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='help_text',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Help text'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='properties',
            field=models.ManyToManyField(blank=True, null=True, related_name='filters', to='catalog.Property', verbose_name='Properties'),
        ),
    ]
