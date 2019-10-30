# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/10 15:19
# 文件名称  : settings.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule

import os
from datetime import date, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_db_uri(dbinfo):
    engine = dbinfo.get('ENGINE') or 'sqlite'
    driver = dbinfo.get('DRIVER') or 'sqlite'
    user = dbinfo.get('USER') or ''
    password = dbinfo.get('PASSWORD') or ''
    host = dbinfo.get('HOST') or ''
    port = dbinfo.get('PORT') or ''
    dbname = dbinfo.get('DBNAME') or ''
    return "{}+{}://{}:{}@{}:{}/{}".format(engine, driver, user, password, host, port, dbname)


class Config:

    DEBUG = False

    TESTING = False
    # 禁止对象追踪修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'ADW'

    SESSION_TYPE = 'redis'

    PERMANENT_SESSION_LIFETIME = 140

    SCHEDULER_API_ENABLED = True

    # 任务列表
    SCHEDULER_JOBS = [
        {  # 第一个任务
            'id': 'job1',
            'func': 'WestffsSchedules.tasks:get_login_his',
            # 'func': 'WestffsSchedules.tasks:get_login_his',

            'args': (date.today()-timedelta(days=1), date.today()-timedelta(days=1)),
            'trigger': 'interval',  # interval表示循环任务
            'seconds': 5,
            # 'trigger': {
            #     'type': 'cron',  # 类型
            #     'day_of_week': "0-6",  # 可定义具体哪几天要执行
            #     'hour': '1',  # 小时数
            #     'minute': '0'
            # }
        },
        {  # 第二个任务，每隔5S执行一次
            'id': 'method_test',
            'func': 'WestffsSchedules.tasks:method_test',  # 方法名
            'args': (1, 2, 'job2'),  # 入参
            'trigger': 'interval',  # interval表示循环任务
            'seconds': 5,
        }
    ]


class DevelopConfig(Config):

    # DEBUG = True
    dbinfo = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '62.234.1.36',
        'PORT': '3306',
        'DBNAME': 'flask03',
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestConfig(Config):

    TESTING = True
    dbinfo = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '62.234.1.36',
        'PORT': '3306',
        'DBNAME': 'flask02',
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class ProductConfig(Config):

    dbinfo = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '62.234.1.36',
        'PORT': '3306',
        'DBNAME': 'flask03',
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class StagingConfig(Config):

    dbinfo = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '62.234.1.36',
        'PORT': '3306',
        'DBNAME': 'flask02',
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


envs = {
    'develop': DevelopConfig,
    'testing': TestConfig,
    'staging': StagingConfig,
    'product': ProductConfig,
    'default': DevelopConfig,
}