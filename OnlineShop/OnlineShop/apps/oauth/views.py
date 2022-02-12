import logging
from django import http
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from QQLoginTool.QQtool import OAuthQQ

from OnlineShop.settings.common import config_qq
from OnlineShop.utils.common import gen_access_token
from OnlineShop.utils.response_code import RETCODE
from oauth.models import OauthQQUser

logger = logging.getLogger("django")


# Create your views here.
class QQAuthUserView(View):

    def get(self, request):
        # 获取Authorization Code
        code = request.GET.get("code")
        if not code:
            return http.HttpResponse("缺少code")
            # 创建工具对象
        oauth = OAuthQQ(client_id=config_qq.qq_client_id,
                        client_secret=config_qq.qq_client_secret,
                        redirect_uri=config_qq.qq_redirect_uri,
                        )
        try:
            # 使用code向QQ服务器请求access_token
            access_token = oauth.get_access_token(code)
            # 使用access_token向qq服务器请求openid
            openid = oauth.get_access_token(access_token)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('OAuth2.0认证失败')

        # 判断openid是否绑定过用户
        try:
            oauth_user = OauthQQUser.objects.get(openid=openid)
        except OauthQQUser.DoesNotExist:
            # 如果openid没有绑定商城用户
            access_token = gen_access_token(openid)
            context = {'access_token': access_token}
            return render(request, 'oauth_callback.html', context)
        else:
            # 如果openid绑定商城用户
            # 登录
            login(request, oauth_user.user)
            # 重定向到state
            next_url = request.GET.get("state")
            response = redirect(next_url)
            response.set_cookie("username", oauth_user.user.username, max_age=3600 * 24 * 15)

            return response


class QQAuthURLView(View):

    def get(self, request):
        # 接受next
        next_url = request.GET.get('next')
        # 创建工具对象
        oauth = OAuthQQ(client_id=config_qq.qq_client_id,
                        client_secret=config_qq.qq_client_secret,
                        redirect_uri=config_qq.qq_redirect_uri,
                        state=next_url)
        # 生成QQ登录扫码链接地址
        login_url = oauth.get_qq_url()
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'login_url': login_url})
