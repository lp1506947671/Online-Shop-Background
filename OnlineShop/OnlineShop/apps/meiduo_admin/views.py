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
