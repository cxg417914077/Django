"""gulishop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from rest_framework import routers
from goods.views import GoodsViewSet, CategoryViewSet
from django.views.static import serve
from gulishop.settings import MEDIA_ROOT
from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token
from users.views import VerfyCodeViewSet, UserProfileViewSet
from operations.views import UserFavViewSet, UserLeavingMessingViewSet, UserAddressViewSet
from trade.views import ShopCartViewSet, OrderInfoViewSet, AlipayView

router = routers.DefaultRouter()
router.register(r'goods', GoodsViewSet, base_name='goods')
router.register(r'categorys', CategoryViewSet, base_name='categorys')
router.register(r'code', VerfyCodeViewSet, base_name='code')
router.register(r'users', UserProfileViewSet, base_name='users')
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')
router.register(r'messages', UserLeavingMessingViewSet, base_name='messages')
router.register(r'address', UserAddressViewSet, base_name='address')
router.register(r'shopcarts', ShopCartViewSet, base_name='shopcarts')
router.register(r'orders', OrderInfoViewSet, base_name='orders')

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    # url(r'^goods/$', GoodsViewSet.as_view({'get': 'list'})),
    url(r'', include(router.urls)),
    url(r'^login/', obtain_jwt_token),
    url(r'^alipay_return/$', AlipayView.as_view(), name='alipay_return'),
]
