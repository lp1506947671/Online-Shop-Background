#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import re_path
from rest_framework_jwt.views import obtain_jwt_token

from .views import UserTotalCountView

app_name = "meiduo_admin"
urlpatterns = [
    # 登录
    re_path(r"authorizations", obtain_jwt_token),
    re_path(r"statistical/total_count", UserTotalCountView.as_view()),
]
