from rest_framework import serializers
from .models import VerifyCode, UserProfile
import re
from gulishop.settings import MOBILE_RE
from datetime import datetime
from rest_framework.validators import UniqueValidator


class VerfyCodeSerializer(serializers.ModelSerializer):
    def validate_mobile(self, mobile):
        com = re.compile(MOBILE_RE)
        valid = com.match(mobile)
        if not valid:
            raise serializers.ValidationError('手机号不正确')
        user_mobile = UserProfile.objects.filter(mobile=mobile)
        if user_mobile:
            raise serializers.ValidationError('手机号已注册')
        vcode = VerifyCode.objects.filter(mobile=mobile).order_by('add_time')
        if vcode:
            ti = (datetime.now() - vcode[-1].add_time).seconds
            if ti <= 60:
                raise serializers.ValidationError(f'验证码已发送，请{60-ti}秒后重新发送')
            else:
                vcode.delete()
        return mobile

    class Meta:
        model = VerifyCode
        fields = ['mobile']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=30, min_length=11, validators=[UniqueValidator(queryset=UserProfile.objects.all())])
    password = serializers.CharField(required=True, max_length=15, min_length=6, write_only=True, style={'input_type': 'password'})
    code = serializers.CharField(required=True, max_length=6, min_length=6, write_only=True)

    def validate_code(self, code):
        mobile = self.initial_data['username']
        code_list = VerifyCode.objects.filter(mobile=mobile, code=code).order_by('-add_time')
        if code_list:
            last_code = code_list[0]
            if (datetime.now() - last_code.add_time).seconds > 1800:
                raise serializers.ValidationError('验证码已过期，请重新获取')
        else:
            raise serializers.ValidationError('手机或验证码有误')

    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'code']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'birthday', 'gender', 'email', 'mobile']

