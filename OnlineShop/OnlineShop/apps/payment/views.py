import os

from alipay import AliPay
from django import http
from django.shortcuts import render

# Create your views here.
# 测试账号：pqcanx4910@sandbox.com
from django.views import View

from orders.models import OrderInfo
from OnlineShop.settings.common import config_alipay
from OnlineShop.utils.common import LoginRequiredJSONMixin
from OnlineShop.utils.response_code import RETCODE


class PaymentView(LoginRequiredJSONMixin, View):
    """订单支付功能"""

    def get(self, request, order_id):
        # 查询要支付的订单
        user = request.user
        try:
            order = OrderInfo.objects.get(
                order_id=order_id,
                user=user,
                status=OrderInfo.ORDER_STATUS_ENUM["UNPAID"],
            )
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden("订单信息错误")

        # 创建支付宝支付对象
        alipay = AliPay(
            appid=config_alipay.alipay_appid,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"
            ),
            alipay_public_key_path=os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "keys/alipay_public_key.pem"
            ),
            sign_type="RSA2",
            debug=config_alipay.alipay_debug,
        )

        # 生成登录支付宝连接
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject="XiaoPawnYe%s" % order_id,
            return_url=config_alipay.alipay_return_url,
        )

        # 响应登录支付宝连接
        # 真实环境电脑网站支付网关：https://openapi.alipay.com/gateway.do? + order_string
        # 沙箱环境电脑网站支付网关：https://openapi.alipaydev.com/gateway.do? + order_string
        alipay_url = config_alipay.alipay_url + "?" + order_string
        return http.JsonResponse(
            {"code": RETCODE.OK, "errmsg": "OK", "alipay_url": alipay_url}
        )
