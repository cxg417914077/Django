from rest_framework.response import Response
from .models import ShopCart, OrderInfo, OrderGoods
from rest_framework import mixins, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permission import IsOwnerOrReadOnly
from .serializers import ShopCartListSerializer, ShopCartSerializer, OrderInfoSerializer, OrderInfoListSerializer
import time, random


class ShopCartViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartListSerializer
        else:
            return ShopCartSerializer

    def get_queryset(self):
        return ShopCart.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        goods = serializer.validated_data['goods']
        nums = serializer.validated_data['nums']

        shopcart_list = ShopCart.objects.filter(user=self.request.user, goods=goods)

        if shopcart_list:
            shopcart = shopcart_list[0]
            shopcart.nums += nums
        else:
            shopcart = ShopCart()
            shopcart.user = self.request.user
            shopcart.goods = goods
            shopcart.nums = nums
            shopcart.save()

        serializer = self.get_serializer(shopcart)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderInforViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderInfoListSerializer
        else:
            return OrderInfoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 创建订单
        orderinfo = OrderInfo.objects.create(**serializer.validated_data)
        orderinfo.order_sn = self.get_order_sn()
        orderinfo.save()
        # 订单商品
        shopcart_list = ShopCart.objects.filter(user=self.request.user)
        for goods in shopcart_list:
            ordergoods = OrderGoods()
            ordergoods.order = orderinfo
            ordergoods.goods = goods.goods
            ordergoods.nums = goods.nums
            ordergoods.save()
        # 清空购物车
        shopcart_list.delete()
        headers = self.get_success_headers(serializer.data)
        serializer = self.get_serializer(orderinfo)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_order_sn(self):
        sn = f'{time.strftime("%Y%m%d%H%M%S")}{self.request.user.id}{random.randint(10, 99)}'
        return sn


