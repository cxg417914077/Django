import xadmin
from xadmin.views import BaseAdminView, CommAdminView
from .models import GoodsCategory, Goods, CategoryBrand, GoodsImage, Banner, Students


class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True


class CommXadminSetting(object):
    site_title = 'GULI商城'
    site_footer = 'CXG出品'
    menu_style = 'accordion'


class GoodsCategoryXadmin(object):
    list_display = ['name', 'category_type', 'code', 'parent_category', 'is_tab', 'add_time']
    model_icon = 'fa fa-shopping-bag'


class GoodsXadmin(object):
    list_display = ['name', 'category', 'goods_sn', 'goods_brief', 'goods_front_image', 'click_num', 'add_time']
    style_fields = {'goods_desc': 'ueditor'}


class CategoryBrandXadmin(object):
    list_display = ['category', 'image', 'name', 'add_time']


class GoodsImageXadmin(object):
    list_display = ['goods', 'image', 'add_time']


class BannerXadmin(object):
    list_display = ['goods', 'image', 'index', 'add_time']


class StudentsXadmin(object):
    list_display = ['name', 'age', 'add_time']


xadmin.site.register(CommAdminView, CommXadminSetting)
xadmin.site.register(BaseAdminView, BaseXadminSetting)
xadmin.site.register(GoodsCategory, GoodsCategoryXadmin)
xadmin.site.register(Goods, GoodsXadmin)
xadmin.site.register(CategoryBrand, CategoryBrandXadmin)
xadmin.site.register(GoodsImage, GoodsImageXadmin)
xadmin.site.register(Banner, BannerXadmin)
xadmin.site.register(Students, StudentsXadmin)
