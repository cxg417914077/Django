import os, sys

dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gulishop.settings")

import django
django.setup()


from db_tools.data.product_data import row_data
from goods.models import Goods, GoodsCategory, GoodsImage


for item in row_data:
    goods = Goods()
    goods.name = item['name']
    goods.goods_brief = item['desc'] if item['desc'] else ''
    goods.goods_desc = item['goods_desc'] if item['goods_desc'] else ''
    goods.market_price = item['market_price'].replace('￥', '').replace('元', '')
    goods.shop_price = item['sale_price'].replace('￥', '').replace('元', '')
    goods.goods_front_image = item['images'][0] if item['images'] else ''

    category_name = item['categorys'][-1]
    category_list = GoodsCategory.objects.filter(name=category_name)
    if category_list:
        goods.category = category_list[0]
    goods.save()

    for image in item['images']:
        goods_image = GoodsImage()
        goods_image.goods = goods
        goods_image.image = image
        goods_image.save()
