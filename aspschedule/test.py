# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/29 14:41
# 文件名称  : test.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
import unittest
from manage import app

class LoginTest(unittest.TestCase):
    """构造单元测试案例"""
    def test_empty_user_pwd(self):
        # 创建进行web请求的客户端
        client = app.test_client()


if __name__ == "__main__":
    unittest.main()

    # inserter = db.insert(table='login_info_his').prefix_with("OR REPLACE")

    # for item in lines:
    #     info = {}
    #     info["Id"] = item.get('Id')
    #     info["Account"] = item.get('Account')
    #     info["Ip"] = item.get('Ip')
    #     info["Address"] = item.get('Address')
    #     info["City"] = item.get('City')
    #     info["LoginTime"] = item.get('LoginTime').replace('T', ' ')
    #     info["LeaveTime"] = item.get('LeaveTime').replace('T', ' ')
    #     info["OnlineMinute"] = item.get('OnlineMinute')
    #     city_list = city_cut(info.get("City"))
    #     if len(city_list) == 1:
    #         info["province"] = city_list[0]
    #     else:
    #         info["province"] = city_list[0]
    #         info["city_name"] = city_list[1]
    #     infos.append(info)
    # for item in lines:
    #     info = LoginInfo()
    #     info.Id = item.get('Id')
    #     info.Account = item.get('Account')
    #     info.Ip = item.get('Ip')
    #     info.Address = item.get('Address')
    #     info.City = item.get('City')
    #     info.LoginTime = item.get('LoginTime').replace('T', ' ')
    #     info.LeaveTime = item.get('LeaveTime').replace('T', ' ')
    #     info.OnlineMinute = item.get('OnlineMinute')
    #     city_list = city_cut(info.City)
    #     if len(city_list) == 1:
    #         info.province = city_list[0]
    #     else:
    #         info.province = city_list[0]
    #         info.city_name = city_list[1]
    #     infos.append(info)
    #
    # db.session.add_all(infos).values("REPLACE")
    # db.session.commit()
    # db.session.execute(
    #     LoginInfo.__table__.insert().values("REPLACE"),
    #     infos
    # )
    # db.session.commit()