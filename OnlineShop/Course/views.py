from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .serializers import CategorySerializer


# Create your views here.


class CategoryView(APIView):

    def get(self, request):
        # 通过ORM操作获取所有分类数据
        queryset = models.Category.objects.all()
        # 利用序列化器去序列化我们的数据
        ser_obj = CategorySerializer(queryset, many=True)

        return Response(ser_obj.data)
