import xadmin
from users.models import VerifyCode


class VerifyCodeXadmin(object):
    list_display = ['mobile', 'code', 'add_time']


xadmin.site.register(VerifyCode, VerifyCodeXadmin)

