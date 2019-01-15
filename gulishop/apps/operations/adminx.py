import xadmin
from .models import UserFav, UserLeavingMessing, UserAddress


class UserFavXadmin(object):
    list_play = ['user', 'goods', 'add_time']
    model_icon = 'fa fa-opera'


class UserLeavingMessingXadmin(object):
    list_play = ['user', 'msg_type', 'subject', 'message', 'file', 'add_time']


class UserAddressXadmin(object):
    list_play = ['user', 'province', 'city', 'district', 'signing_name', 'signing_mobile', 'address', 'add_time']


xadmin.site.register(UserFav, UserFavXadmin)
xadmin.site.register(UserAddress, UserAddressXadmin)
xadmin.site.register(UserLeavingMessing, UserLeavingMessingXadmin)

