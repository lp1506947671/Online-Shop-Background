from datetime import date
from rest_framework.response import Response

from rest_framework.views import APIView

# Create your views here.
from users.models import User


class UserTotalCountView(APIView):
    def get(self, request):
        now_date = date.today()
        count = User.objects.all().count()
        return Response({"count": count, "date": now_date})


class UserDayCountView(APIView):
    def get(self, request):
        # 获取当前日期
        now_date = date.today()
        # 获取当日注册用户数量 date_joined 记录创建账户时间
        count = User.objects.filter(date_joined__gte=now_date).count()
        return Response({"count": count, "date": now_date})
