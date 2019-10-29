# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/29 11:36
# 文件名称  : jobs.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
import datetime

import requests

from WestffsSchedules.ext import db, scheduler
from WestffsSchedules.models import LoginInfo
from WestffsSchedules.utils.city_cut import city_cut


def method_test(a, b, c):
    print(datetime.datetime.now())
    print('begin')
    print(a+b, c)


def get_login_his(startTime, endTime):
    page = 1
    payload = {'orderBy': '-id', 'startTime': startTime, 'endTime': endTime}
    while True:
        url_login_info = r"http://47.75.133.250/api/Values/GetLoginInfoLog/100/%d" % page
        print(url_login_info)
        # logger.info("login_info url地址：%s" % url_login_info)
        page = page + 1
        resp = requests.get(url_login_info, params=payload, timeout=(50, 100)).json()
        # html_json = requests.get(url_login_info, timeout=(5, 10)).json()
        try:
            lines = resp.get('rows')
        except Exception as e:
            print("get data error")
            return

        if len(lines) == 0:
            return

        # inserter = db.insert(table='login_info_his').prefix_with("OR REPLACE")

        param = []
        for index in lines:
            print(index)
            city_list = city_cut(index.get("City"))
            if len(city_list) == 1:
                index["province"] = city_list[0]
                index["city_name"] = ''
            else:
                index["province"] = city_list[0]
                index["city_name"] = city_list[1]
            para = "(%s, %d, '%s', '%s', '%s', '%s', '%s', %d, '%s', '%s')" % \
                   (index.get('Id'), index.get('Account'), index.get('Ip'), index.get('Address'), index.get('City'),
                    index.get('LoginTime'), index.get('LeaveTime'), index.get('OnlineMinute'), index.get('province'),
                    index.get('city_name'))
            param.append(para)

        params = ','.join(param)
        SQL = "REPLACE INTO login_info_log(id, account, ip, address, city, login_time, leave_time, online_minute, " \
              "province, city_name) VALUES %s" % params

        db.session.execute(SQL)
        db.session.commit()

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