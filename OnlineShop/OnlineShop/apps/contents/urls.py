#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import re_path

from contents import views

app_name = "contents"
urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
]
