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
]
