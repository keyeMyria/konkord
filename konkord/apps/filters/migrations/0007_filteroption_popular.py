# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filters', '0006_auto_20170127_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='filteroption',
            name='popular',
            field=models.BooleanField(default=False, verbose_name='Popular'),
        ),
    ]
