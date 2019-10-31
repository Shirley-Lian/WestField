# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/29 11:36
# 文件名称  : jobs.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
import datetime

import pandas as pd
import requests

from WestffsSchedules.ext import db, scheduler
from WestffsSchedules.models import LoginInfo, Mt4List, UserInfo

from WestffsSchedules.utils.city_cut import get_city
from WestffsSchedules.utils.mails import PySendMail

engine = db.get_engine()

def method_test(a, b, c):
    print(datetime.datetime.now())
    print('begin')
    print(a+b, c)


def url_request_resp(api, items, page, data):
    url = r"http://47.75.133.250/api/Values/%s/%d/%d" % (api, items, page)
    print(url)
    # logger.info("login_info url地址：%s" % url_login_info)
    resp = requests.get(url, params=data, timeout=(50, 100)).json()
    # html_json = requests.get(url_login_info, timeout=(5, 10)).json()
    try:
        lines = resp.get('rows')
    except Exception as e:
        print("get data error")
        lines = ''
        return lines
    return lines


def get_login_his(startTime, endTime):
    page = 1
    payload = {'orderBy': '-id', 'startTime': startTime, 'endTime': endTime}
    api = 'GetLoginInfoLog'
    items = 100

    while True:
        lines = url_request_resp(api, items, page, payload)
        page = page + 1
        if len(lines) == 0:
            return

        param = []
        for index in lines:
            print(index)
            city_list = get_city(index.get("City"))

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


def get_login_last():
    page = 1
    payload ={}
    api = 'GetLoginInfo'
    items = 100
    userids = []
    usernames = []
    address = []
    accounts = []
    log_address = []
    log_time = []
    data = {
        'UserID': userids,
        'UserName': usernames,
        '注册地址': address,
        '登陆账号': accounts,
        '登陆地址': log_address,
        '最后一次登陆时间': log_time,
    }
    while True:
        lines = url_request_resp(api, items, page, payload)
        if len(lines) == 0:
            break
        page = page + 1

        param = []
        for index in lines:

            words_list = get_city(index.get('City'))

            province = words_list[0]
            city_detail = words_list[1]

            if index.get('LoginTime')[:10] == datetime.date.today().strftime('%Y-%m-%d'):

                account = index.get('Account')

                mt4list = Mt4List.query.filter_by(account=account).first()

                if mt4list and mt4list.group_name not in ['W-SystemTest', 'W-Test']:

                    user_id = mt4list.user_id

                    userinfo = UserInfo.query.filter_by(user_id=user_id).first()

                    if userinfo and userinfo.province != province:
                        userids.append(user_id)
                        usernames.append(userinfo.name)
                        address.append(userinfo.address)
                        accounts.append(account)
                        log_address.append(index.get("City"))
                        log_time.append(index.get("LoginTime"))

                #
                # user_address = db.session.execute("select province from userinfo where user_id=%d" % user_id)

            para = "(%s, %d, '%s', '%s', '%s', '%s', %d, '%s', '%s')" % (index.get('Id'), index.get('Account'),
                                                                         index.get('Ip'), index.get('Address'),
                                                                         index.get('City'), index.get('LoginTime'),
                                                                         index.get('OnlineMinute'), province,
                                                                         city_detail)
            param.append(para)

        params = ','.join(param)
        SQL = "REPLACE INTO login_lastinfo VALUES %s" % params
        db.session.execute(SQL)
        db.session.commit()

    frame = pd.DataFrame(data)
    df_html = frame.to_html(escape=False)
    # print(df_html)
    title = u"注册地址与登陆地址不相符"
    warn_type = u"异地登陆预警"
    # mailadd = "zhangh0725@gmail.com"
    mailadd = "lianxiaorui0511@163.com"
    # mailadd = "dofuy007@gmail.com"
    sendmail = PySendMail()
    ret = sendmail.mail(df_html, mailadd, warn_type, title)
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")

