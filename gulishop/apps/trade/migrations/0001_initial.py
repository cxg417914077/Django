# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-15 20:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nums', models.IntegerField(verbose_name='商品数量')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '订单商品信息',
                'verbose_name_plural': '订单商品信息',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_sn', models.CharField(max_length=50, unique=True, verbose_name='订单唯一编号')),
                ('order_mount', models.FloatField(verbose_name='订单总价')),
                ('order_message', models.CharField(blank=True, max_length=300, null=True, verbose_name='订单留言')),
                ('trade_no', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='交易流水号')),
                ('trade_status', models.CharField(choices=[('PAYING', '待支付'), ('TRADE_SUCESS', '支付成功'), ('TRADE_CLOSE', '支付关闭'), ('TRADE_FAIL', '支付失败'), ('TRADE_FINSHED', '交易结束')], default='PAYING', max_length=20, verbose_name='订单状态')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='支付时间')),
                ('signing_name', models.CharField(max_length=20, verbose_name='收货人姓名')),
                ('signing_mobile', models.CharField(max_length=11, verbose_name='联系电话')),
                ('address', models.CharField(max_length=200, verbose_name='收货地址')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
            },
        ),
        migrations.CreateModel(
            name='ShopCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(verbose_name='购买数量')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='所属商品')),
            ],
            options={
                'verbose_name': '购物车信息',
                'verbose_name_plural': '购物车信息',
            },
        ),
    ]
