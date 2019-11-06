# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/11/6 11:14
# 文件名称  : __init__.py.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
from flask_restful import Api

from WestffsSchedules.apis.warning_api import SafeAccountResource, SafeAccountsResource, AddSafeAccountResource
# from WestffsSchedules.apis.user_api import HelloResource, UserResource

api = Api()


def init_api(app):
    api.init_app(app=app)


api.add_resource(SafeAccountResource, "/safeact/<int:account>/")
api.add_resource(SafeAccountsResource, "/white/accounts/<int:page>/")
api.add_resource(AddSafeAccountResource, "/addsafe/accounts/")
