# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/10 15:20
# 文件名称  : ext.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

db = SQLAlchemy()
mail = Mail()

scheduler = APScheduler()


def init_ext(app):
    # 加上下面的代码，定时任务才可以执行
    db.app = app
    db.init_app(app=app)

    mail.init_app(app=app)

    scheduler.init_app(app=app)
    scheduler.start()