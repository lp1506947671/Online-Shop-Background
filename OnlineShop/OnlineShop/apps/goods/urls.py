#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import re_path

from . import views

app_name = "goods"
urlpatterns = [
    # 商品列表
    re_path(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$', views.ListView.as_view(), name="list"),
    re_path(r'^hot/(?P<category_id>\d+)/$', views.HotGoodsView.as_view(), name="hot"),
    re_path(r"^detail/(?P<sku_id>\d+)/$", views.DetailView.as_view(), name="detail"),
    re_path(r"^detail/visit/(?P<category_id>\d+)/", views. DetailVisitView.as_view())
]
