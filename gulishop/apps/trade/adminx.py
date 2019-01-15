import xadmin
from .models import ShopCart, OrderInfo, OrderGoods


class ShopCartXadmin(object):
    list_display = ['user', 'goods', 'num', 'add_time']
    model_icon = 'fa fa-shopping-cart'


class OrderInfoXadmin(object):
    list_display = ['user', 'order_sn', 'order_mount', 'order_message', 'trade_no', 'trade_status', 'pay_time', 'signing_name', 'signing_mobile', 'address', 'add_time']


class OrderGoodsXadmin(object):
    list_display = ['order', 'goods', 'nums', 'add_time']


xadmin.site.register(ShopCart, ShopCartXadmin)
xadmin.site.register(OrderInfo, OrderInfoXadmin)
xadmin.site.register(OrderGoods, OrderGoodsXadmin)
