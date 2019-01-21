from rest_framework import serializers
from .models import UserFav, UserLeavingMessing, UserAddress
from goods.serializers import GoodsSerializer


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%y-%m-%d %H:%M:%S')

    class Meta:
        model = UserFav
        fields = '__all__'


class UserFavListSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = UserFav
        fields = '__all__'


class UserLeavingMessingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%y-%m-%d %H:%M:%S')

    class Meta:
        model = UserLeavingMessing
        fields = '__all__'


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%y-%m-%d %H:%M:%S')

    class Meta:
        model = UserAddress
        fields = '__all__'

