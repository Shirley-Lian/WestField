# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/11/6 11:17
# 文件名称  : warning_api.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule

from flask import request, current_app
from flask_restful import Resource, marshal_with, fields, abort

from WestffsSchedules.models import WarningLoginInfo

warning_fields = {
    "account": fields.Integer,
    "city": fields.String,
    "code": fields.Integer,
    # "name": fields.String(attribute="g_name"),
}

single_warning_fields = {
    "data": fields.Nested(warning_fields),
    "status": fields.Integer,
    "msg": fields.String,
}
multi_warning_fields = {
    "data": fields.List(fields.Nested(warning_fields)),
    "status": fields.Integer,
    "msg": fields.String,
    "pages": fields.Integer,
    "items": fields.Integer,
}


class SafeAccountResource(Resource):

    @marshal_with(single_warning_fields)
    def get(self, account):
        warn_act = WarningLoginInfo.query.filter_by(account=account).first()
        print(warn_act.city)

        data = {
            "status": 200,
            "msg": "ok",
            "data": warn_act,
        }

        return data

    def post(self):

        account = request.values.get('account')
        warn_act = WarningLoginInfo.query.filter_by(account=account).first()

        if not warn_act:
            # abort(404)
            abort(404, message="account doesn't exist", msg="fail")

        if not warn_act.delete():
            abort(404)

        data = {
            "msg": "delete success",
            "status": 204
        }

        current_app.logger.info('delete {} from white list'.format(account))

        return data


class AddSafeAccountResource(Resource):

    @marshal_with(single_warning_fields)
    def post(self):

        account = request.values.get('account')
        city = ''
        code = 1

        warn_act = WarningLoginInfo()

        warn_act.account = account
        warn_act.city = city
        warn_act.code = code

        if not warn_act.save():
            abort(400)

        data = {
            "msg": "create success",
            "status": 200,
            # "data": marshal(good, goods_fields),
            "data": warn_act,
        }
        return data


class SafeAccountsResource(Resource):

    @marshal_with(multi_warning_fields)
    def get(self, page):
        try:
            warn_acts = WarningLoginInfo.query.filter(WarningLoginInfo.code.__eq__(1)).paginate(page, 10)

        except Exception as e:
            print(e)
            data = {
                "status": 404,
                "msg": "fail",
                "pages": 0,
                "items": 0,
            }
            return data

        # 总页数
        num = warn_acts.pages
        # 总条数
        acts = warn_acts.total
        if not warn_acts:
            abort(404, message="goods doesn't exist", msg="fail")
        data = {
            "status": 200,
            "msg": "ok",
            "data": warn_acts.items,
            "pages": num,
            "items": acts,
        }

        return data

    # def delete(self, id):
    #
    #     goods = Goods.query.get(id)
    #
    #     if not goods:
    #         # abort(404)
    #         abort(404, message="goods doesn't exist", msg="fail")
    #
    #     if not goods.delete():
    #         abort(404)
    #
    #     data = {
    #         "msg": "delete success",
    #         "status": 204
    #     }
    #     return data
    #
    # def put(self, id):
    #
    #     goods = Goods.query.get(id)
    #
    #     if not goods:
    #         abort(404)
    #
    #     g_name = request.form.get("g_name")
    #     g_price = request.form.get("g_price")
    #
    #     goods.g_name = g_name
    #     goods.g_price = g_price
    #
    #     if not goods.save():
    #         abort(404)
    #
    #     data = {
    #         "msg": "add success",
    #         "status": 201,
    #         "data": goods,
    #     }
    #
    #     return marshal(data, single_goods_fields)
    #
    # @marshal_with(single_goods_fields)
    # def patch(self, id):
    #
    #     goods = Goods.query.get(id)
    #
    #     if not goods:
    #         abort(404)
    #
    #     g_name = request.form.get("g_name")
    #     g_price = request.form.get("g_price")
    #
    #     goods.g_name = g_name or goods.g_name
    #     goods.g_price = g_price or goods.g_price
    #
    #     if not goods.save():
    #         abort(404)
    #
    #     data = {
    #         "msg": "add success",
    #         "status": 201,
    #         "data": goods,
    #     }
    #
    #     return data