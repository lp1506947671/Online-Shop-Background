#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from OnlineShop.settings.common import global_config, MyDict
from celery_tasks.sms.yuntongxing.CCPRestSDK import REST


def sendTemplateSMS(to, data, temp_id):
    """
    :param to: 手机号码
    :param data: 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填
    :param temp_id:模板Id
    :return:
    """
    config = MyDict(global_config.verifications)
    # 初始化REST SDK
    rest = REST(config.server_ip, config.server_port, config.soft_version)
    rest.setAccount(config.account_sid, config.account_token)
    rest.setAppId(config.app_id)

    result = rest.sendTemplateSMS(to, data, temp_id)
    for k, v in result.items():
        if k == 'templateSMS':
            for x, y in v.items():
                print('%s:%s' % (x, y))
        else:
            print('%s:%s' % (k, v))