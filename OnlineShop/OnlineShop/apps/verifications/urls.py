#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import re_path

from verifications import views

app_name = "verifications"
urlpatterns = [
    # 图形验证码
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
]
