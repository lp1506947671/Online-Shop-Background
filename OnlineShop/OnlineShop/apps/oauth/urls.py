#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import re_path

from contents import views
from oauth.views import QQAuthUserView, QQAuthURLView

app_name = "oauth"
urlpatterns = [
    re_path("^qq/login/$", QQAuthURLView.as_view()),
    re_path("^oauth_callback/$", QQAuthUserView.as_view())
]
