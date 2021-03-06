# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static_pages', '0004_auto_20170217_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagecategory',
            name='meta_h1',
            field=models.TextField(blank=True, null=True, verbose_name='Meta H1'),
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='meta_description',
            field=models.TextField(blank=True, null=True, verbose_name='Meta description'),
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='meta_description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Meta description'),
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='meta_description_uk',
            field=models.TextField(blank=True, null=True, verbose_name='Meta description'),
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='meta_keywords',
            field=models.TextField(blank=True, null=True, verbose_name='Meta keywords'),
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='meta_keywords_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Meta keywords'),
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='meta_keywords_uk',
            field=models.TextField(blank=True, null=True, verbose_name='Meta keywords'),
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='meta_seo_text',
            field=models.TextField(blank=True, null=True, verbose_name='SEO text'),
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='meta_seo_text_ru',
            field=models.TextField(blank=True, null=True, verbose_name='SEO text'),
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='meta_seo_text_uk',
            field=models.TextField(blank=True, null=True, verbose_name='SEO text'),
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='meta_title',
            field=models.TextField(blank=True, null=True, verbose_name='Meta title'),
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='meta_title_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Meta title'),
        ),
        migrations.AlterField(
            model_name='pagecategory',
            name='meta_title_uk',
            field=models.TextField(blank=True, null=True, verbose_name='Meta title'),
        ),
    ]
