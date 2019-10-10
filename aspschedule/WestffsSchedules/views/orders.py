# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/10 15:23
# 文件名称  : orders.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
from flask import Blueprint

order = Blueprint('order', __name__)


@order.route('/')
def hello_world():
    return 'Hello World!'