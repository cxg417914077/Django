# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-21 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodscategory',
            old_name='is_tad',
            new_name='is_tab',
        ),
        migrations.AlterField(
            model_name='goodscategory',
            name='category_type',
            field=models.IntegerField(choices=[(1, '一级'), (2, '二级'), (3, '三级')], verbose_name='类别级别'),
        ),
    ]
