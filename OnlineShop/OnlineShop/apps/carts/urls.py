#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import re_path

from carts import views

app_name = "carts"
urlpatterns = [
    re_path("^carts/$", views.CartsView.as_view(), name="info"),
    re_path("^carts/selection/$", views.CartsSelectAllView.as_view()),
    re_path("^carts/simple/$", views.CartsSimpleView.as_view()),
]
