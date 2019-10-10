# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/10 15:21
# 文件名称  : __init__.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
from WestffsSchedules.views.orders import order


def init_view(app):
    app.register_blueprint(order)