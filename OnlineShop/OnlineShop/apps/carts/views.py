import json
from itsdangerous import Serializer, base64_encode, base64_decode
from django import http
from django.views import View
from django.shortcuts import render
from django_redis import get_redis_connection
from goods import models
from OnlineShop.settings import constants
from OnlineShop.settings.dev import SECRET_KEY
from OnlineShop.utils.response_code import RETCODE

# Create your views here.

s = Serializer(SECRET_KEY)


class CartsSimpleView(View):
    """商品页面右上角购物车"""

    def get(self, request):
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询Redis购物车
            redis_conn = get_redis_connection("carts")
            redis_cart = redis_conn.hgetall("carts_%s" % user.id)
            cart_selected = redis_conn.smembers("selected_%s" % user.id)
            # 将redis中的两个数据统一格式，跟cookie中的格式一致，方便统一查询
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    "count": int(count),
                    "selected": sku_id in cart_selected,
                }
        else:
            # 用户未登录，查询cookie购物车
            cart_str = request.COOKIES.get("carts")
            if cart_str:
                # cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
                cart_dict = s.loads(base64_decode(cart_str.encode()))
            else:
                cart_dict = {}

        # 构造简单购物车JSON数据
        cart_skus = []
        sku_ids = cart_dict.keys()
        skus = models.SKU.objects.filter(id__in=sku_ids)
        for sku in skus:
            cart_skus.append(
                {
                    "id": sku.id,
                    "name": sku.name,
                    "count": cart_dict.get(sku.id).get("count"),
                    "default_image_url": sku.default_image.url,
                }
            )

        # 响应json列表数据
        return http.JsonResponse(
            {"code": RETCODE.OK, "errmsg": "OK", "cart_skus": cart_skus}
        )


class CartsSelectAllView(View):
    """全选购物车"""

    def put(self, request):
        # 接收和校验参数
        json_dict = json.loads(request.body.decode())
        selected = json_dict.get("selected", True)
        # 校验参数
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden("参数selected有误")
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，操作redis购物车
            redis_conn = get_redis_connection("carts")
            cart = redis_conn.hgetall("carts_%s" % user.id)
            sku_id_list = cart.keys()
            if selected:
                # 全选
                redis_conn.sadd("selected_%s" % user.id, *sku_id_list)
            else:
                # 取消全选
                redis_conn.srem("selected_%s" % user.id, *sku_id_list)
            return http.JsonResponse({"code": RETCODE.OK, "errmsg": "全选购物车成功"})
        else:
            # 用户未登录，操作cookie购物车
            cart = request.COOKIES.get("carts")
            response = http.JsonResponse({"code": RETCODE.OK, "errmsg": "全选购物车成功"})
            if cart is not None:
                # cart = pickle.loads(base64.b64decode(cart.encode()))
                cart = s.loads(base64_decode(cart.encode()))
                for sku_id in cart:
                    cart[sku_id]["selected"] = selected
                # cookie_cart = base64.b64encode(pickle.dumps(cart)).decode()
                cookie_cart = base64_encode(s.dumps(cart).encode()).decode()
                response.set_cookie(
                    "carts", cookie_cart, max_age=constants.CARTS_COOKIE_EXPIRES
                )

            return response


class CartsView(View):
    """购物车管理"""

    def get(self, request):
        """展示购物车"""
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询redis购物车
            redis_conn = get_redis_connection("carts")
            # 获取redis中的购物车数据
            redis_cart = redis_conn.hgetall("carts_%s" % user.id)
            # 获取redis中的选中状态
            cart_selected = redis_conn.smembers("selected_%s" % user.id)

            # 将redis中的数据构造成跟cookie中的格式一致，方便统一查询
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                cart_dict[str(int(sku_id))] = {
                    "count": int(count),
                    "selected": sku_id in cart_selected,
                }
        else:
            # 用户未登录，查询cookies购物车
            cart_str = request.COOKIES.get("carts")
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                # cart_dict = s.loads(base64.b64decode(cart_str.encode()))
                cart_dict = s.loads(base64_decode(cart_str.encode()))
            else:
                cart_dict = {}

        # 构造购物车渲染数据
        sku_ids = cart_dict.keys()
        skus = models.SKU.objects.filter(id__in=sku_ids)
        cart_skus = []
        for sku in skus:
            sku_id_str = str(sku.id)
            cart_skus.append(
                {
                    "id": sku.id,
                    "name": sku.name,
                    "count": cart_dict.get(sku_id_str).get("count"),
                    "selected": str(
                        cart_dict.get(sku_id_str).get("selected")
                    ),  # 将True，转'True'，方便json解析
                    "default_image_url": sku.default_image.url,
                    "price": str(sku.price),  # 从Decimal('10.2')中取出'10.2'，方便json解析
                    "amount": str(sku.price * cart_dict.get(sku_id_str).get("count")),
                }
            )

        context = {
            "cart_skus": cart_skus,
        }

        # 渲染购物车页面
        return render(request, "cart.html", context)

    def post(self, request):
        """添加购物车"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get("sku_id")
        count = json_dict.get("count")
        selected = json_dict.get("selected", True)

        # 判断参数是否齐全
        if not all([sku_id, count]):
            return http.HttpResponseForbidden("缺少必传参数")
        # 判断sku_id是否存在
        try:
            models.SKU.objects.get(id=sku_id)
        except models.SKU.DoesNotExist:
            return http.HttpResponseForbidden("商品不存在")
        # 判断count是否为数字
        try:
            count = int(count)
        except Exception:
            return http.HttpResponseForbidden("参数count有误")
        # 判断selected是否为bool值
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden("参数selected有误")

        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，操作redis购物车
            redis_conn = get_redis_connection("carts")
            pl = redis_conn.pipeline()
            # 新增购物车数据
            pl.hincrby("carts_%s" % user.id, sku_id, count)
            # 新增选中的状态
            if selected:
                pl.sadd("selected_%s" % user.id, sku_id)
            # 执行管道
            pl.execute()
            # 响应结果
            return http.JsonResponse({"code": RETCODE.OK, "errmsg": "添加购物车成功"})
        else:
            # 用户未登录，操作cookie购物车
            cart_str = request.COOKIES.get("carts")
            # 如果用户操作过cookie购物车
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                # cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
                cart_dict = s.loads(base64_decode(cart_str.encode()))
            else:  # 用户从没有操作过cookie购物车
                cart_dict = {}

            # 判断要加入购物车的商品是否已经在购物车中,如有相同商品，累加求和，反之，直接赋值
            if sku_id in cart_dict:
                # 累加求和
                origin_count = cart_dict[sku_id]["count"]
                count += origin_count
            cart_dict[sku_id] = {"count": count, "selected": selected}
            # 将字典转成bytes,再将bytes转成base64的bytes,最后将bytes转字符串
            # cookie_cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
            cookie_cart_str = base64_encode(s.dumps(cart_dict).encode()).decode()

            # 创建响应对象
            response = http.JsonResponse({"code": RETCODE.OK, "errmsg": "添加购物车成功"})
            # 响应结果并将购物车数据写入到cookie
            response.set_cookie(
                "carts", cookie_cart_str, max_age=constants.CARTS_COOKIE_EXPIRES
            )
            return response

    def put(self, request):
        """修改购物车"""
        # 接收和校验参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get("sku_id")
        count = json_dict.get("count")
        selected = json_dict.get("selected", True)
        # 判断参数是否齐全
        if not all([sku_id, count]):
            return http.HttpResponseForbidden("缺少必传参数")
        # 判断sku_id是否存在
        try:
            sku = models.SKU.objects.get(id=sku_id)
        except models.SKU.DoesNotExist:
            return http.HttpResponseForbidden("商品sku_id不存在")
        # 判断count是否为数字
        try:
            count = int(count)
        except Exception:
            return http.HttpResponseForbidden("参数count有误")
        # 判断selected是否为bool值
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden("参数selected有误")

        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，修改redis购物车
            redis_conn = get_redis_connection("carts")
            pl = redis_conn.pipeline()
            # 因为接口设计为幂等的，直接覆盖
            pl.hset("carts_%s" % user.id, sku_id, count)
            # 是否选中
            if selected:
                pl.sadd("selected_%s" % user.id, sku_id)
            else:
                pl.srem("selected_%s" % user.id, sku_id)
            pl.execute()

            # 创建响应对象
            cart_sku = {
                "id": sku_id,
                "count": count,
                "selected": selected,
                "name": sku.name,
                "default_image_url": sku.default_image.url,
                "price": sku.price,
                "amount": sku.price * count,
            }
            return http.JsonResponse(
                {"code": RETCODE.OK, "errmsg": "修改购物车成功", "cart_sku": cart_sku}
            )
        else:
            # 用户未登录，修改cookie购物车
            cart_str = request.COOKIES.get("carts")
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                # cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
                cart_dict = s.loads(base64_decode(cart_str.encode()))
            else:
                cart_dict = {}
            # 因为接口设计为幂等的，直接覆盖
            cart_dict[sku_id] = {"count": count, "selected": selected}
            # 将字典转成bytes,再将bytes转成base64的bytes,最后将bytes转字符串
            # cookie_cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
            cookie_cart_str = base64_encode(s.dumps(cart_dict).encode()).decode()
            # 创建响应对象
            cart_sku = {
                "id": sku_id,
                "count": count,
                "selected": selected,
                "name": sku.name,
                "default_image_url": sku.default_image.url,
                "price": sku.price,
                "amount": sku.price * count,
            }
            response = http.JsonResponse(
                {"code": RETCODE.OK, "errmsg": "修改购物车成功", "cart_sku": cart_sku}
            )
            # 响应结果并将购物车数据写入到cookie
            response.set_cookie(
                "carts", cookie_cart_str, max_age=constants.CARTS_COOKIE_EXPIRES
            )
            return response

    def delete(self, request):
        """删除购物车"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get("sku_id")

        # 判断sku_id是否存在
        try:
            models.SKU.objects.get(id=sku_id)
        except models.SKU.DoesNotExist:
            return http.HttpResponseForbidden("商品不存在")

        # 判断用户是否登录
        user = request.user
        if user is not None and user.is_authenticated:
            # 用户未登录，删除redis购物车
            redis_conn = get_redis_connection("carts")
            pl = redis_conn.pipeline()
            # 删除键，就等价于删除了整条记录
            pl.hdel("carts_%s" % user.id, sku_id)
            pl.srem("selected_%s" % user.id, sku_id)
            pl.execute()

            # 删除结束后，没有响应的数据，只需要响应状态码即可
            return http.JsonResponse({"code": RETCODE.OK, "errmsg": "删除购物车成功"})
        else:
            # 用户未登录，删除cookie购物车
            cart_str = request.COOKIES.get("carts")
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                # cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
                cart_dict = s.loads(base64_decode(cart_str.encode()))
            else:
                cart_dict = {}

            # 创建响应对象
            response = http.JsonResponse({"code": RETCODE.OK, "errmsg": "删除购物车成功"})
            if sku_id in cart_dict:
                del cart_dict[sku_id]
                # 将字典转成bytes,再将bytes转成base64的bytes,最后将bytes转字符串
                # cookie_cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
                cookie_cart_str = base64_encode(s.dumps(cart_dict).encode()).decode()
                # 响应结果并将购物车数据写入到cookie
                response.set_cookie(
                    "carts", cookie_cart_str, max_age=constants.CARTS_COOKIE_EXPIRES
                )
            return response
