# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/10 15:23
# 文件名称  : orders.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
from flask import Blueprint, request
from flask_mail import Message

from WestffsSchedules.ext import mail
from WestffsSchedules.models import LoginInfo, TestModel, WarningLoginInfo
from WestffsSchedules.utils.mails import PySendMail

order = Blueprint('order', __name__)


@order.route('/')
def hello_world():
    return 'Hello World!'


# @order.route('/mail/')
# def send_email(df):
#     title = "注册地址与登陆地址不相符"
#     warn_type = "异地登陆预警"
#     text = PySendMail().mail(df_html=df, warning_type=warn_type, title=title)
#     msg = Message("flask", recipients=["lianxiaorui0511@163.com",])
#     msg.body = "from flask"
#     # msg.html = "<h2>字体加粗<h2>"
#     msg.html = text
#     mail.send(message=msg)
#     return "邮件发送成功"


@order.route('/test/')
def test():
    test = TestModel.query.with_entities(TestModel.name).all()
    # test = TestModel.query.all()
    print(test)
    print('1111')
    print(type(test))
    for item in test:
        print(item)
        print(item.name)
    return " success "


@order.route('/addSafeAccount/')
def add_white_list():
    account = request.args.get("Account")
    warn_act = WarningLoginInfo.query.filter_by(account=account).first()
    warn_act.code = 1
    warn_act.save()
    return "添加成功"


