from .models import VerifyCode, UserProfile
from rest_framework import viewsets, mixins, status
from .serializers import VerfyCodeSerializer, UserProfileSerializer, UserListSerializer
import random
from rest_framework.response import Response
from utils.yunpian import YunPian
from gulishop.settings import YUNPIAN_KEY
from rest_framework_jwt.settings import api_settings
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated


class VerfyCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = VerfyCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        code = self.get_code()

        yunpian = YunPian(YUNPIAN_KEY)
        result = yunpian.send_code(mobile, code)
        if result['code'] == 0:
            verifycode = VerifyCode()
            verifycode.mobile = mobile
            verifycode.code = code
            verifycode.save()
            return Response(data={'mobile': mobile, 'msg': result['msg']}, status=status.HTTP_201_CREATED)
        return Response(data={'mobile': mobile, 'msg': result['msg']}, status=status.HTTP_400_BAD_REQUEST)

    def get_code(self):
        str = '1234567890'
        code = ''
        for i in range(6):
            code += random.choice(str)
        return code


class UserProfileViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            return []
        else:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserProfileSerializer
        else:
            return UserListSerializer

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserProfile()
        user.username = serializer.validated_data['username']
        user.set_password(serializer.validated_data['password'])
        user.mobile = user.username
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        ret = serializer.data
        ret['name'] = user.name if user.name else user.username
        ret['token'] = token
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

