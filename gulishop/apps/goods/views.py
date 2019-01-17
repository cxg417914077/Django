from .models import Goods
from .filter import GoodsFilter
from .serializers import GoodsSerializer
from rest_framework import mixins, filters, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


class GoodsPagination(PageNumberPagination):
    page_size = 10
    # max_page_size = 100
    page_query_param = 'pn'
    page_size_query_param = 'page_size'


class GoodsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    pagination_class = GoodsPagination
    serializer_class = GoodsSerializer
    # 过滤器
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = GoodsFilter
    # 搜索字段
    search_fields = ['name', 'goods_brief', 'desc']
    # 排序字段
    ordering_fields = ['shop_price', 'sold_num']



