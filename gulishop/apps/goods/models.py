from django.db import models
from datetime import datetime

# Create your models here.


class GoodsCategory(models.Model):
    name = models.CharField(max_length=20, verbose_name='商品类别名称')
    category_type = models.CharField(choices=((1, '一级'), (2, '二级'), (3, '三级')), max_length=10, verbose_name='类别级别')
    code = models.CharField(max_length=50, verbose_name='类别编号')
    parent_category = models.ForeignKey('self', null=True, blank=True, verbose_name='所属上级类别', related_name='sub_cat')
    is_tad = models.BooleanField(default=False, verbose_name='是否导航')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品类别信息'
        verbose_name_plural = verbose_name


class Goods(models.Model):
    category = models.ForeignKey(GoodsCategory, verbose_name='所属类别', related_name='goods')
    name = models.CharField(max_length=100, verbose_name='商品名称')
    goods_sn = models.CharField(max_length=30, unique=True, verbose_name='商品唯一编号', null=True, blank=True)
    goods_brief = models.CharField(max_length=300, null=True, blank=True, verbose_name='商品简介')
    desc = models.TextField(null=True, blank=True, verbose_name='商品详情')
    good_front_image = models.ImageField(upload_to='goods/images', max_length=200, verbose_name='商品封面详情')
    market_price = models.FloatField(verbose_name='商品市场价')
    shop_price = models.FloatField(verbose_name='商品店铺价')
    ship_free = models.BooleanField(default=True, verbose_name='是否包邮')
    click_num = models.IntegerField(default=0, verbose_name='商品访问量')
    fav_num = models.IntegerField(default=0, verbose_name='商品收藏数')
    goods_num = models.IntegerField(default=100, verbose_name='商品库存')
    sold_num = models.IntegerField(default=0, verbose_name='商品销售数量')
    is_hot = models.BooleanField(default=False, verbose_name='是否热卖')
    is_new = models.BooleanField(default=False, verbose_name='是否新品')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品详情信息'
        verbose_name_plural = verbose_name


class CategoryBrand(models.Model):
    category = models.ForeignKey(GoodsCategory, verbose_name='所属类别', related_name='brands')
    image = models.ImageField(upload_to='brand/images', max_length=200, verbose_name='赞助图片')
    name = models.CharField(max_length=50, verbose_name='赞助名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '赞助信息'
        verbose_name_plural = verbose_name


class GoodsImage(models.Model):
    goods = models.ForeignKey(Goods, verbose_name='所属商品', related_name='images')
    image = models.ImageField(upload_to='goods/images', max_length=200, verbose_name='商品轮播图片')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = '商品轮播图信息'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    goods = models.ForeignKey(Goods, verbose_name='所属商品', related_name='banners')
    image = models.ImageField(upload_to='goods/images', max_length=200, verbose_name='首页轮播图片')
    index = models.IntegerField(verbose_name='轮播顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.goods.name

    class Meta:
        verbose_name = '首页轮播图信息'
        verbose_name_plural = verbose_name

