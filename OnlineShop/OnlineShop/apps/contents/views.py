# Create your views here.
from django.http import HttpResponse
from django.views import View


class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        return HttpResponse("ok")
