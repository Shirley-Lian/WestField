# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/10 15:23
# 文件名称  : orders.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
from flask import Blueprint, request

from WestffsSchedules.models import LoginInfo, TestModel, WarningLoginInfo


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


# @order.route('/test/')
def test():
    # get_login_h
    # is()
    # test = TestModel.query.with_entities(TestModel.name).all()
    # # test = TestModel.query.all()
    # print(test)
    # print('1111')
    # print(type(test))
    # for item in test:
    #     print(item)
    #     print(item.name)
    return " success "


# @order.route('/addSafeAccount/')
def add_white_list():
    """
    将账号加入白名单
    """
    account = request.args.get("Account")
    warn_act = WarningLoginInfo.query.filter_by(account=account).first()
    if warn_act:
        warn_act.code = 1
        warn_act.save()
    else:
        warn_act = WarningLoginInfo()
        warn_act.account = account
        warn_act.city = ''
        warn_act.code = 1
        warn_act.save()
    return "添加成功"


# @order.route('/remove/SafeAccount/')
def remove_white_list():
    """
    将账号移除白名单
    """
    account = request.args.get("Account")
    try:
        warn_act = WarningLoginInfo.query.filter_by(account=account).first()
        if warn_act:
            warn_act.code = 0
            warn_act.save()
        else:
            warn_act = WarningLoginInfo()
            warn_act.account = account
            warn_act.city = ''
            warn_act.code = 0
            warn_act.save()
    except Exception as e:
        print(e)
        return "添加失败"
    return "添加成功"


