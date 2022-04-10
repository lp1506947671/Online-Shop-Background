import logging
import re

from django import http
from django.contrib.auth import login
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from django_redis import get_redis_connection

from OnlineShop.settings.common import config_qq
from OnlineShop.utils.common import gen_access_token, check_access_token
from OnlineShop.utils.response_code import RETCODE
from carts.utils import merge_cart_cookie_to_redis
from oauth.models import OauthQQUser
from users.models import User

logger = logging.getLogger("django")


# Create your views here.
class QQAuthUserView(View):
    def get(self, request):
        # 获取Authorization Code
        code = request.GET.get("code")
        if not code:
            return http.HttpResponse("缺少code")
            # 创建工具对象
        oauth = OAuthQQ(
            client_id=config_qq.qq_client_id,
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
            return http.HttpResponseServerError("OAuth2.0认证失败")

        # 判断openid是否绑定过用户
        try:
            oauth_user = OauthQQUser.objects.get(openid=openid)
        except OauthQQUser.DoesNotExist:
            # 如果openid没有绑定商城用户
            access_token = gen_access_token(openid)
            context = {"access_token": access_token}
            return render(request, "oauth_callback.html", context)
        else:
            # 如果openid绑定商城用户
            # 登录
            login(request, oauth_user.user)
            # 重定向到state
            next_url = request.GET.get("state")
            response = redirect(next_url)
            response.set_cookie(
                "username", oauth_user.user.username, max_age=3600 * 24 * 15
            )

            return response

    def post(self, request):
        """美多商城用户绑定到openid"""
        # 接收参数
        mobile = request.POST.get("mobile")
        pwd = request.POST.get("password")
        sms_code_client = request.POST.get("sms_code")
        access_token = request.POST.get("access_token")

        # 校验参数
        # 判断参数是否齐全
        if not all([mobile, pwd, sms_code_client]):
            return http.HttpResponseForbidden("缺少必传参数")
        # 判断手机号是否合法
        if not re.match(r"^1[3-9]\d{9}$", mobile):
            return http.HttpResponseForbidden("请输入正确的手机号码")
        # 判断密码是否合格
        if not re.match(r"^[0-9A-Za-z]{8,20}$", pwd):
            return http.HttpResponseForbidden("请输入8-20位的密码")
        # 判断短信验证码是否一致
        redis_conn = get_redis_connection("verify_code")
        sms_code_server = redis_conn.get("sms_%s" % mobile)
        if sms_code_server is None:
            return render(
                request, "oauth_callback.html", {"sms_code_errmsg": "无效的短信验证码"}
            )
        if sms_code_client != sms_code_server.decode():
            return render(
                request, "oauth_callback.html", {"sms_code_errmsg": "输入短信验证码有误"}
            )
        # 判断openid是否有效：错误提示放在sms_code_errmsg位置
        openid = check_access_token(access_token)
        if not openid:
            return render(
                request, "oauth_callback.html", {"openid_errmsg": "无效的openid"}
            )

        # 保存注册数据
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 用户不存在,新建用户
            user = User.objects.create_user(
                username=mobile, password=pwd, mobile=mobile
            )
        else:
            # 如果用户存在，检查用户密码
            if not user.check_password(pwd):
                return render(
                    request, "oauth_callback.html", {"account_errmsg": "用户名或密码错误"}
                )

        # 将用户绑定openid
        try:
            OauthQQUser.objects.create(openid=openid, user=user)
        except DatabaseError:
            return render(request, "oauth_callback.html", {"qq_login_errmsg": "QQ登录失败"})

        # 实现状态保持
        login(request, user)

        # 响应绑定结果
        next = request.GET.get("state")
        response = redirect(next)
        response = merge_cart_cookie_to_redis(
            request=request, user=user, response=response
        )
        # 登录时用户名写入到cookie，有效期15天
        response.set_cookie("username", user.username, max_age=3600 * 24 * 15)

        return response


class QQAuthURLView(View):
    def get(self, request):
        # 接受next
        next_url = request.GET.get("next")
        # 创建工具对象
        oauth = OAuthQQ(
            client_id=config_qq.qq_client_id,
            client_secret=config_qq.qq_client_secret,
            redirect_uri=config_qq.qq_redirect_uri,
            state=next_url,
        )
        # 生成QQ登录扫码链接地址
        login_url = oauth.get_qq_url()
        return http.JsonResponse(
            {"code": RETCODE.OK, "errmsg": "OK", "login_url": login_url}
        )
