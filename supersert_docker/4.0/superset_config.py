# -*- coding: utf-8 -*-
"""
    Created by w at 2024/1/25.
    Description:
    Changelog: all notable changes to this file will be documented
"""
# 将默认的数据库改为postgresql
# 不能是dws产品，只能是pg库，建表语句不兼容
import os
from typing import Optional


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)


DATABASE_DIALECT = get_env_variable("DATABASE_DIALECT")
DATABASE_USER = get_env_variable("DATABASE_USER")
DATABASE_PASSWORD = get_env_variable("DATABASE_PASSWORD")
DATABASE_HOST = get_env_variable("DATABASE_HOST")
DATABASE_PORT = get_env_variable("DATABASE_PORT")
DATABASE_DB = get_env_variable("DATABASE_DB")
SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
    DATABASE_DIALECT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DB,
)

# 2.1以及以上的版本要求SECRET_KEY
SECRET_KEY = "5MrCzW6GduMGIUTn4d7e6DP7b0hJ2C1b6YApAP0TJKBcp6Yeh6dDa2n1"
# 登录安全策略 https://superset.apache.org/docs/security/
TALISMAN_CONFIG = {
    "content_security_policy": {
        "default-src": ["'self'"],
        "img-src": ["'self'", "data:"],
        "worker-src": ["'self'", "blob:"],
        "connect-src": ["'self'"],
        "object-src": "'none'",
        "style-src": ["'self'", "'unsafe-inline'"],
        "script-src": ["'self'", "'strict-dynamic'"],
    },
    "content_security_policy_nonce_in": ["script-src"],
    "force_https": False,
    "session_cookie_secure": False,
}
# 启用语言切换
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "zh": {"flag": "cn", "name": "Chinese"},
}
# 特性配置
FEATURE_FLAGS = {
    "ALERTS_ATTACH_REPORTS": True,
    "ALLOW_ADHOC_SUBQUERY": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DASHBOARD_RBAC (docs)": True,
    "DATAPANEL_CLOSED_BY_DEFAULT": True,
    "DISABLE_LEGACY_DATASOURCE_EDITOR": True,
    "DRUID_JOINS": True,
    "EMBEDDABLE_CHARTS": True,
    "EMBEDDED_SUPERSET": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ESCAPE_MARKDOWN_HTML": True,
    "LISTVIEWS_DEFAULT_CARD_VIEW": True,
    "SCHEDULED_QUERIES": True,
    "SQLLAB_BACKEND_PERSISTENCE": True,
    "SQL_VALIDATORS_BY_ENGINE": True,
    "THUMBNAILS": True,
    "THUMBNAILS_SQLA_LISTENERS": True,
    "DASHBOARD_CACHE": True
    # 开启 Jinja SQL 模板功能。文档：https://superset.apache.org/docs/installation/sql-templating/
}
# 缓存配置
REDIS_HOST = get_env_variable("REDIS_HOST")
CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 24,
    "CACHE_KEY_PREFIX": "superset_cache_",
    "CACHE_REDIS_HOST": "%s" % REDIS_HOST,
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 0,
    "CACHE_REDIS_URL": "redis://%s:6379/0" % REDIS_HOST,
}

DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 24,
    "CACHE_KEY_PREFIX": "superset_data_",
    "CACHE_REDIS_HOST": "%s" % REDIS_HOST,
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 0,
    "CACHE_REDIS_URL": "redis://%s:6379/0" % REDIS_HOST,
}

FILTER_STATE_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_filter_',
    'CACHE_REDIS_URL': 'redis://%s:6379/2' % REDIS_HOST,
}

# 缓存缩略图 https://superset.apache.org/docs/installation/async-queries-celery/
THUMBNAIL_SELENIUM_USER = "admin"

THUMBNAIL_CACHE_CONFIG = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 24 * 60 * 60 * 7,
    "CACHE_KEY_PREFIX": "thumbnail_",
    "CACHE_NO_NULL_WARNING": True,
    "CACHE_REDIS_URL": "redis://%s:6379/0" % REDIS_HOST,
}


class CeleryConfig(object):
    BROKER_URL = "redis://%s:6379/0" % REDIS_HOST
    CELERY_IMPORTS = (
        "superset.sql_lab",
        "superset.tasks",
        "superset.tasks.thumbnails",
    )
    CELERY_RESULT_BACKEND = "redis://%s:6379/0" % REDIS_HOST
    CELERYD_PREFETCH_MULTIPLIER = 10
    CELERY_ACKS_LATE = True


CELERY_CONFIG = CeleryConfig

# chrome
WEBDRIVER_TYPE = "chrome"
WEBDRIVER_OPTION_ARGS = [
    "--force-device-scale-factor=2.0",
    "--high-dpi-support=2.0",
    "--headless",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-extensions",
]

WEBDRIVER_BASEURL = "http://localhost:8088/"
WEBDRIVER_BASEURL_USER_FRIENDLY = "http://localhost:8088"
