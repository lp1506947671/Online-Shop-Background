#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import re_path

from users import views

app_name = "users"
urlpatterns = [

    re_path(r'^register/$', views.RegisterView.as_view(), name='register'),
]
