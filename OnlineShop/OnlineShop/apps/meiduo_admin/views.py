from datetime import date
from rest_framework.response import Response

from rest_framework.views import APIView

# Create your views here.
from orders.models import OrderInfo
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


class UserActiveCountView(APIView):
    def get(self, request):
        # 获取当前日期
        now_date = date.today()
        # 获取当日登录用户数量  last_login记录最后登录时间
        count = User.objects.filter(last_login__gte=now_date).count()
        return Response({"count": count, "date": now_date})


class UserOrderCountView(APIView):
    def get(self, request):
        # 获取当前日期
        now_date = date.today()
        # 获取当日下单用户数量  orders__create_time 订单创建时间
        count = (
            OrderInfo.objects.filter(create_time__gte=now_date)
            .values("user_id")
            .count()
        )
        return Response({"count": count, "date": now_date})
