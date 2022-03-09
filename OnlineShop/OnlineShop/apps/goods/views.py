from django import http
from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import render
from django.views import View
# Create your views here.
from goods import models
from goods.utils import get_breadcrumb
from utils.contents_utils import get_categories


class ListView(View):
    """商品列表页"""

    def get(self, request, category_id, page_num):
        """提供商品列表页"""
        # 判断category_id是否正确
        try:
            category = models.GoodsCategory.objects.get(id=category_id)
        except models.GoodsCategory.DoesNotExist:
            return http.HttpResponseNotFound('GoodsCategory does not exist')

        # 查询商品频道分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(category)

        # 渲染页面
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb
        }
        return render(request, 'list.html', context)
