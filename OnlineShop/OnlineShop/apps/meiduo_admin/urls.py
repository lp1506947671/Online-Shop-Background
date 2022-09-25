#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import re_path
from rest_framework_jwt.views import obtain_jwt_token

from . import views

app_name = "meiduo_admin"
urlpatterns = [
    # 登录
    re_path(r"authorizations", obtain_jwt_token),
    # 用户总数统计
    re_path(r"statistical/total_count", views.UserTotalCountView.as_view()),
    # 日增用户统计
    re_path(r"statistical/day_increment", views.UserDayCountView.as_view()),
    # 日活跃用户统计
    re_path(r"statistical/day_active", views.UserDayCountView.as_view()),
    # 日下单用户量统计
    re_path(r"statistical/day_orders", views.UserOrderCountView.as_view()),
    # 日分类商品访问量月增用户统计
    re_path(r"statistical/month_increment", views.UserMonthCountView.as_view()),
]
