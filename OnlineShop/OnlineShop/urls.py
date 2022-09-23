"""OnlineShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^search/", include("haystack.urls")),
    re_path(r"^", include("contents.urls", namespace="contents")),
    re_path(r"^", include("users.urls", namespace="users")),
    # verifications
    re_path(r"^", include("verifications.urls")),
    # oauth
    re_path(r"^", include("oauth.urls", namespace="oauth")),
    # areas
    re_path(r"^", include("areas.urls", namespace="areas")),
    # goods
    re_path(r"^", include("goods.urls", namespace="goods")),
    # carts
    re_path(r"^", include("carts.urls", namespace="carts")),
    # orders
    re_path(r"^", include("orders.urls", namespace="orders")),
    # payment
    re_path(r"^", include("payment.urls", namespace="payment")),
    # meiduo_admin
    re_path(r"^", include("meiduo_admin.urls", namespace="payment")),
]
