#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import http
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from itsdangerous import TimedJSONWebSignatureSerializer, BadData

from OnlineShop.settings import constants
from OnlineShop.settings.common import config_email
from OnlineShop.utils.response_code import RETCODE


def gen_access_token(openid):
    """将openid进行序列化"""
    s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
    data = {'openid': openid}
    token = s.dumps(data)
    return token.decode()


def check_access_token(access_token_openid):
    """将access_token_openid进行反序列化"""
    s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
    try:
        data = s.loads(access_token_openid)
    except BadData:  # openid密文过期
        return None
    else:
        # 放回openid明文
        return data.get("openid")


def generate_verify_email_url(user):
    """
    生成邮箱验证链接
    :param user: 当前登录用户
    :return: verify_url
    """
    serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=constants.ACCESS_TOKEN_EXPIRES)
    data = {'user_id': user.id, 'email': user.email}
    token = serializer.dumps(data).decode()
    verify_url = config_email.email_verify_url + '?token=' + token
    return verify_url


class LoginRequiredJSONMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})
