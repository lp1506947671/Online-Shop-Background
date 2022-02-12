#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer, BadData

from OnlineShop.settings import constants


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
