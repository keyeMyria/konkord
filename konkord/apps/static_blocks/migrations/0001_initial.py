# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaticBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=255, verbose_name='Identifier')),
                ('content', models.TextField(verbose_name='Content')),
                ('content_ru', models.TextField(null=True, verbose_name='Content')),
                ('content_uk', models.TextField(null=True, verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Static block',
                'verbose_name_plural': 'Static blocks',
            },
        ),
    ]
