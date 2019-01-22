from rest_framework import viewsets, mixins
from .models import UserFav, UserLeavingMessing, UserAddress
from .serializers import UserFavSerializer, UserFavListSerializer, UserLeavingMessingSerializer, UserAddressSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permission import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavListSerializer
        else:
            return UserFavSerializer


class UserLeavingMessingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = UserLeavingMessingSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return UserLeavingMessing.objects.filter(user=self.request.user)


class UserAddressViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


