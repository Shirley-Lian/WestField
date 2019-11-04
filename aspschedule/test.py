# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/29 14:41
# 文件名称  : test.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
import unittest

import requests
import datetime

import socket
from manage import app


class LoginTest(unittest.TestCase):
    """构造单元测试案例"""
    def test_empty_user_pwd(self):
        # 创建进行web请求的客户端
        client = app.test_client()


def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        # ip = s.gethostname()[0]

    finally:
        s.close()

    return ip


import fcntl
import struct


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


if __name__ == '__main__':
    s = socket.socket()
    host = socket.gethostname()
    print(host)
    print(get_host_ip())
    print(get_ip_address("virbr0"))
    # unittest.main()
    # d = '2019-03-29T16:17:56.123'
    # print(d[11:13])
    # x = datetime.datetime.strptime(d[:19], '%Y-%m-%dT%H:%M:%S').timestamp()
    # print(x)

    # page = 1
    # startData = endDate = '2019-10-31' #datetime.date.today()
    # payload = {'startData': startData, 'endDate': endDate}
    # api = 'GetLoginInfo'
    # items = 100
    # url = r"http://47.75.133.250/api/Values/%s/%d/%d" % (api, items, page)
    # print(url)
    # # logger.info("login_info url地址：%s" % url_login_info)
    # resp = requests.get(url, params=payload, timeout=(50, 100)).json()
    # # html_json = requests.get(url_login_info, timeout=(5, 10)).json()
    # print(resp)

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
    #     user = Userinfo()
    #     user.Id = index.get('Id')
    #     user.Account = index.get('Account')
    #     user.Ip = index.get('Ip')
    #     user.Address = index.get('Address')
    #     user.City = index.get('City')
    #     user.LoginTime = index.get('LoginTime').replace('T', ' ')
    #     user.LeaveTime = index.get('LeaveTime').replace('T', ' ')
    #     user.OnlineMinute = index.get('OnlineMinute')
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