# Create your views here.
import random
import logging
from django import http
from django.views import View
from django_redis import get_redis_connection

from OnlineShop.settings.common import global_config, MyDict
from OnlineShop.utils.response_code import RETCODE
from verifications.libs.captcha.captcha import captcha
from verifications.libs.yuntongxing.SendTemplateSMS import sendTemplateSMS

CONFIG = MyDict(global_config.verifications)
logger = logging.getLogger("django")


class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid: 唯一标识图形验证码所属于的用户
        :return: image/jpg
        """

        # 生成图片验证码
        text, image = captcha.generate_captcha()
        print(text)
        # 保存图片验证码
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, CONFIG.image_code_redis_expires, text)

        # 响应图片验证码
        return http.HttpResponse(image, content_type='image/jpg')


class SMSCodeView(View):
    """短信验证码"""

    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param mobile: 手机号
        :return: JSON
        """
        # 接收参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')

        # 校验参数
        if not all([image_code_client, uuid]):
            return http.JsonResponse({'code': RETCODE.NECESSARYPARAMERR, 'errmsg': '缺少必传参数'})

        # 创建连接到redis的对象
        redis_conn = get_redis_connection('verify_code')
        pl = redis_conn.pipeline()

        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '发送短信过于频繁'})

        # 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            # 图形验证码过期或者不存在
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码失效'})
        # 删除图形验证码，避免恶意测试图形验证码

        try:
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)
        # 对比图形验证码
        image_code_server = image_code_server.decode()  # bytes转字符串
        if image_code_client.lower() != image_code_server.lower():  # 转小写后比较
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码有误'})

        # 生成短信验证码：生成6位数验证码
        sms_code = '%06d' % random.randint(0, 999999)
        print(sms_code)
        # 保存短信验证码
        pl.setex('sms_%s' % mobile, CONFIG.sms_code_redis_expires, sms_code)
        # 保存发送短信验证码的标记
        pl.setex('send_flag_%s' % mobile, CONFIG.send_sms_code_interval, 1)
        # 执行请求
        pl.execute()
        # 发送短信验证码
        # sendTemplateSMS(mobile, [sms_code, int(CONFIG.sms_code_redis_expires) // 60], CONFIG.send_sms_template_id)

        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})
