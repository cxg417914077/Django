# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-22 11:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20190121_1201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopcart',
            old_name='num',
            new_name='nums',
        ),
    ]