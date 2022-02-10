from django.db import models
from OnlineShop.utils.models import BaseModel


# Create your models here.
class OauthQQUser(BaseModel):
    """QQ登录用户数据"""
    user = models.ForeignKey(to="users.User", verbose_name="用户", on_delete=models.CASCADE)
    openid = models.CharField(max_length=64, verbose_name="openid", db_index=True)

    class Meta:
        db_table = "oauth_qq_user"
        verbose_name = "QQ登录用户数据"
        verbose_name_plural = verbose_name
