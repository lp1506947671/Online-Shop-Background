#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import re_path

from orders import views

app_name = "orders"
urlpatterns = [
    # 结算订单
    re_path(
        r"^orders/settlement/$", views.OrderSettlementView.as_view(), name="settlement"
    ),
    # 保存订单
    re_path(r"^orders/commit/$", views.OrderCommitView.as_view(), name="commit"),
    # 提交订单成功
    re_path(r"^orders/success/$", views.OrderSuccessView.as_view()),
]
