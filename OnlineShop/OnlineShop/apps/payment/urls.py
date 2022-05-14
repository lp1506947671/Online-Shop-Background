#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import re_path

from payment import views

app_name = "payment"
urlpatterns = [
    re_path(r"^payment/(?P<order_id>\d+)/$", views.PaymentView.as_view()),
    re_path(r"^payment/status/$", views.PaymentStatusView.as_view()),
]
