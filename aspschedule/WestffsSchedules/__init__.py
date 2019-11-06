# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/10 15:18
# 文件名称  : __init__.py.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
from flask import Flask

from WestffsSchedules.apis import init_api
from WestffsSchedules.ext import init_ext
from WestffsSchedules.logger import add_file_logger
from WestffsSchedules.settings import envs

from WestffsSchedules.views import init_view


def create_app(env):
    app = Flask(__name__)

    app.config.from_object(envs.get(env))

    add_file_logger(app)

    # 加载RESTful
    init_api(app)

    init_view(app=app)

    init_ext(app=app)
    # init_mail(app=app)

    return app