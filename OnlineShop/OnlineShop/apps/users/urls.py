#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.urls import re_path

from users import views

app_name = "users"
urlpatterns = [
    # 用户注册: reverse(users:register) == '/register/'
    re_path(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 判断用户名是否重复注册
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    # 判断用户名是否重复注册
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 用户登录
    re_path(r'^login/$', views.LoginView.as_view(), name='login'),
    # 用户退出登录
    re_path(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # 用户中心
    re_path(r'^info/$', login_required(views.UserInfoView.as_view()), name='info'),
    # 添加邮箱
    re_path(r'^emails/$', views.EmailView.as_view()),
    # 验证邮箱
    re_path(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    # 展示用户地址
    re_path(r'^addresses/$', views.AddressView.as_view(), name='address'),
]
