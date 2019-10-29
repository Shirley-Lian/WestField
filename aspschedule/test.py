# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/29 14:41
# 文件名称  : test.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
import requests

from WestffsSchedules.ext import db
from WestffsSchedules.models import LoginInfo


def get_login_his(startTime, endTime):
    page = 1
    payload = {'orderBy': '-id', 'startTime': startTime, 'endTime': endTime}
    city = []
    while True:
        url_login_info = r"http://47.75.133.250/api/Values/GetLoginInfoLog/10/%d" % page
        # logger.info("login_info url地址：%s" % url_login_info)
        page = page + 1
        html_json = requests.get(url_login_info, params=payload, timeout=(50, 100)).json()
        # html_json = requests.get(url_login_info, timeout=(5, 10)).json()
        print(html_json)
        lines = html_json.get('rows')
        if len(lines) == 0:
            break
        # param = []

        db.session.execute(
            LoginInfo.__table__.insert(),
            lines
        )
        db.session.commit()
        # for index in lines:
        #     print(index)
        #     city.append(index.get("City"))
        #     para = "(%s, %d, '%s', '%s', '%s', '%s', '%s', %d)" % (index.get('Id'), index.get('Account'), index.get('Ip'),
        #                                                            index.get('Address'), index.get('City'),
        #                                                            index.get('LoginTime'), index.get('LeaveTime'),
        #                                                            index.get('OnlineMinute'))
        #     param.append(para)

get_login_his('2019-10-28',"2019-10-28")