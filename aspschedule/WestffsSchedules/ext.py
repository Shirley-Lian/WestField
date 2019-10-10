# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/10 15:20
# 文件名称  : ext.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_ext(app):
    db.init_app(app=app)