from .models import Goods, GoodsCategory
from .filter import GoodsFilter
from .serializers import GoodsSerializer, CategorySerializer
from rest_framework import mixins, filters, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


class GoodsPagination(PageNumberPagination):
    page_size = 12
    # max_page_size = 100
    page_query_param = 'page'
    page_size_query_param = 'page_size'


class GoodsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    # 分页器
    pagination_class = GoodsPagination
    # 序列化器
    serializer_class = GoodsSerializer
    # 过滤器
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = GoodsFilter
    # 搜索字段
    search_fields = ['name', 'goods_brief', 'desc']
    # 排序字段
    ordering_fields = ['shop_price', 'sold_num']


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.queryset.filter(category_type=1)



