from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.


class UserProfile(AbstractUser):
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='用户昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name='用户生日')
    gender = models.CharField(max_length=6, choices=(('male', '女'), ('female', '男')), verbose_name='用户性别')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='用户电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class VerifyCode(models.Model):
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='验证手机号')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '手机验证信息'
        verbose_name_plural = verbose_name



