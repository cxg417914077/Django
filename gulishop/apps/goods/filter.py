from .models import Goods
from django_filters import rest_framework as filters
from django.db.models import Q


class GoodsFilter(filters.FilterSet):
    pricemin = filters.NumberFilter(field_name='shop_price', lookup_expr='gte', label='最低价格')
    pricemax = filters.NumberFilter(field_name='shop_price', lookup_expr='lte', label='最高价格')

    top_category = filters.NumberFilter(method='get_top_category')

    def get_top_category(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'top_category']
