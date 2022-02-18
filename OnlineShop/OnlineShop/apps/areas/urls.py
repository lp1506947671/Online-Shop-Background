#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.urls import re_path

from areas import views

app_name = "areas"
urlpatterns = [
    # 省市区三级联动
    re_path(r'^areas/$', views.AreasView.as_view()),
]
