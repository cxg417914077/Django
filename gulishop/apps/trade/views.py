from datetime import datetime
from rest_framework import mixins, viewsets, status, views
from rest_framework.response import Response
from utils.alipay import AliPay
from .models import ShopCart, OrderGoods, OrderInfo
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permission import IsOwnerOrReadOnly
from .serializers import ShopCartSerializer, ShopCartListSerializer, OrderInfoSerializer, OrderInfoListSerializer
import random, time
from gulishop.settings import APPID, APP_NOTIFY_URL, APP_PRIVATE_KEY_PATH, ALIPAY_PUBLIC_KEY_PATH, RETURN_URL


class ShopCartViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShopCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartListSerializer
        else:
            return ShopCartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        goods = serializer.validated_data['goods']
        nums = serializer.validated_data['nums']

        shopcart_list = ShopCart.objects.filter(user=self.request.user, goods=goods)
        if shopcart_list:
            shopcart = shopcart_list[0]
            shopcart.goods = goods
            shopcart.nums += nums
            shopcart.save()
        else:
            shopcart = ShopCart()
            shopcart.user = self.request.user
            shopcart.goods = goods
            shopcart.nums = nums
            shopcart.save()

        headers = self.get_success_headers(serializer.data)
        serializer = self.get_serializer(shopcart)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderInfoViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderInfoListSerializer
        else:
            return OrderInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        alipay = AliPay(
            appid=APPID,
            app_notify_url=APP_NOTIFY_URL,
            app_private_key_path=APP_PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url=RETURN_URL
        )
        url = alipay.direct_pay(
            subject=instance.order_sn,
            # 订单号
            out_trade_no=instance.order_sn,
            # 订单总价
            total_amount=instance.order_mount
        )
        # 沙箱环境
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        ret = serializer.data
        ret['alipay_url'] = re_url
        return Response(ret)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 创建订单
        order = OrderInfo.objects.create(**serializer.validated_data)
        order.order_sn = self.get_order_sn()
        order.save()
        # 创建订单商品
        goods_list = ShopCart.objects.filter(user=self.request.user)
        for goods in goods_list:
            ordergoods = OrderGoods()
            ordergoods.order = order
            ordergoods.goods = goods.goods
            ordergoods.goods_num = goods.nums
            ordergoods.save()
        # 清空购物车
        goods_list.delete()
        # 支付
        alipay = AliPay(
            appid=APPID,
            app_notify_url=APP_NOTIFY_URL,
            app_private_key_path=APP_PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url=RETURN_URL
        )
        url = alipay.direct_pay(
            subject=order.order_sn,
            # 订单号
            out_trade_no=order.order_sn,
            # 订单总价
            total_amount=order.order_mount
        )
        # 沙箱环境
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        headers = self.get_success_headers(serializer.data)
        serializer = self.get_serializer(order)
        ret = serializer.data
        ret['alipay_url'] = re_url
        return Response(ret, status=status.HTTP_201_CREATED, headers=headers)

    def get_order_sn(self):
        sn = f'{time.strftime("%Y%m%d%H%M%S")}{self.request.user.id}{random.randint(10, 99)}'
        return sn


class AlipayView(views.APIView):
    # 如果用网页登陆支付，走这里
    def get(self, request):
        """
        处理支付宝返回的return_url
        :param request:
        :return:
        """

        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value
        # 得到签名
        sign = processed_dict.pop("sign", None)
        # 下面代码拷贝过来

        alipay = AliPay(
            appid=APPID,
            # 异步的通知接口，当在浏览器扫描创建订单后，这个时候关闭页面，此时可以在客户端或者支护宝账号里面看到这个为支付完成的信息
            app_notify_url=RETURN_URL,
            app_private_key_path=APP_PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            # 同步接口，支付成功后会跳转的接口
            return_url=RETURN_URL
        )
        # 验证通过返回True
        verify_result = alipay.verify(processed_dict, sign)
        print("verify_result================", verify_result)
        if verify_result is True:
            # 该交易在支付宝系统中的交易流水号
            trade_no = processed_dict.get("trade_no", None)
            # 商户网站唯一订单号
            order_sn = processed_dict.get("out_trade_no", None)
            pay_status = processed_dict.get("trade_status", 'TRADE_SUCCESS')

            # 根据订单号查找已经存在的订单列表
            exited_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for exited_order in exited_orders:
                exited_order.trade_no = trade_no
                # 修改状态
                exited_order.pay_status = pay_status
                exited_order.pay_time = datetime.now()
                # 保存数据
                exited_order.save()
            # 发一个成功信息给支付宝，否则支付宝会不停的发消息给我们
            return Response("success")

    # 如果用沙箱客户端扫描支付走这里
    def post(self, request):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        # 从post取出数据，把对应
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value
        # 得到签名
        sign = processed_dict.pop("sign", None)
        # 下面代码拷贝过来

        alipay = AliPay(
            appid=APPID,
            # 异步的通知接口，当在浏览器扫描创建订单后，这个时候关闭页面，此时可以在客户端或者支护宝账号里面看到这个为支付完成的信息
            app_notify_url=RETURN_URL,
            app_private_key_path=APP_PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            # 同步接口，支付成功后会跳转的接口
            return_url=RETURN_URL
        )

        verify_result = alipay.verify(processed_dict, sign)
        if verify_result is True:
            # 该交易在支付宝系统中的交易流水号
            trade_no = processed_dict.get("trade_no", None)
            # 商户网站唯一订单号
            order_sn = processed_dict.get("out_trade_no", None)
            pay_status = processed_dict.get("pay_status", 'TRADE_SUCCESS')

            # 根据订单号查找已经存在的订单列表
            exited_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for exited_order in exited_orders:
                exited_order.trade_no = trade_no
                # 修改状态
                exited_order.pay_status = pay_status
                exited_order.pay_time = datetime.now()
                # 保存数据
                exited_order.save()
            # 发一个成功信息给支付宝，否则支付宝会不停的发消息给我们
            return Response("success")
