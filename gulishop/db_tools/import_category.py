import os, sys


dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gulishop.settings")

import django
django.setup()

from db_tools.data.category_data import row_data
from goods.models import GoodsCategory

for lev1 in row_data:
    cat1 = GoodsCategory()
    cat1.name = lev1['name']
    cat1.code = lev1['code'] if lev1['code'] else ''
    cat1.category_type = 1
    cat1.save()
    for lev2 in lev1['sub_categorys']:
        cat2 = GoodsCategory()
        cat2.name = lev2['name']
        cat2.code = lev2['code'] if lev1['code'] else ''
        cat2.category_type = 2
        cat2.parent_category = cat1
        cat2.save()
        for lev3 in lev2['sub_categorys']:
            cat3 = GoodsCategory()
            cat3.name = lev3['name']
            cat3.code = lev3['code'] if lev1['code'] else ''
            cat3.category_type = 3
            cat3.parent_category = cat2
            cat3.save()
