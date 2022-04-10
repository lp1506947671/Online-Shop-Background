"""
Django settings for OnlineShop project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import sys
import os
from pathlib import Path
from OnlineShop.settings.common import config_email, config_db, config_redis

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 追加导包路径
sys.path.insert(0, os.path.join(BASE_DIR, "OnlineShop", "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-sc#hj4*%nkf&m2%7qrxro@org8f2ojoszc&-34s%9ql7k@pn)w"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["www.xiaopawnye.site", "127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "haystack",
    "users",
    "contents",
    "verifications",
    "oauth",
    "areas",
    "goods",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "OnlineShop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "environment": "OnlineShop.utils.jinja2_env.jinja2_environment",
        },
    },
]

WSGI_APPLICATION = "OnlineShop.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "192.168.190.2",  # 数据库主机
        "PORT": 3306,  # 数据库端口
        "USER": "ossuser",  # 数据库用户名
        "PASSWORD": config_db.password,  # 数据库用户密码
        "NAME": "Online_Shop",  # 数据库名字
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
# 配置静态文件加载路径
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 缓存
CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.190.2:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": config_redis.password,
        },
    },
    "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.190.2:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": config_redis.password,
        },
    },
    "verify_code": {  # 验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.190.2:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": config_redis.password,
        },
    },
    "carts": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.190.2:6379/4",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": config_redis.password,
        },
    },
    "history": {  # 用户浏览记录
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.190.2:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": config_redis.password,
        },
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# 日志
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # 是否禁用已经存在的日志器
    "formatters": {  # 日志信息显示的格式
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(module)s %(lineno)d %(message)s"},
    },
    "filters": {  # 对日志进行过滤
        "require_debug_true": {  # django在debug模式下才输出日志
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {  # 日志处理方法
        "console": {  # 向终端中输出日志
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {  # 向文件中输出日志
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/run.log"),  # 日志文件的位置
            "maxBytes": 300 * 1024 * 1024,
            "backupCount": 10,
            "formatter": "verbose",
        },
    },
    "loggers": {  # 日志器
        "django": {  # 定义了一个名为django的日志器
            "handlers": ["console", "file"],  # 可以同时向终端与文件中输出日志
            "propagate": True,  # 是否继续传递日志信息
            "level": "INFO",  # 日志器接收的最低日志级别
        },
    },
}
AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ["users.utils.UsernameMobileAuthBackend"]
LOGIN_URL = "/login/"

# 指定邮件后端
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.163.com"  # 发邮件主机
EMAIL_PORT = 25  # 发邮件端口
# 授权的邮箱
EMAIL_HOST_USER = config_email.email_host_user
# 邮箱授权时获得的密码，非注册登录密码
EMAIL_HOST_PASSWORD = config_email.email_host_password
EMAIL_FROM = f"OnlineShop<{config_email.email_host_user}>"  # 发件人抬头
# 指定自定义的Django文件存储类
DEFAULT_FILE_STORAGE = "OnlineShop.utils.fastdfs.fdfs_storage.FastDFSStorage"
# FastDFS相关参数
FDFS_BASE_URL = "http://192.168.190.2:8888/"

# Haystack
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine",
        "URL": "http://192.168.190.2:9200/",  # Elasticsearch服务器ip地址，端口号固定为9200
        "INDEX_NAME": "online_shop",  # Elasticsearch建立的索引库的名称
    },
}
# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"
# 控制每页显示数量
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5
