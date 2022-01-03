#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
]
