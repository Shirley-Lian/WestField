# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/29 11:36
# 文件名称  : jobs.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
import datetime
import time
from datetime import date, timedelta

import pandas as pd
import requests

from WestffsSchedules.ext import db
from WestffsSchedules.models import LoginInfo, Mt4List, UserInfo, WarningLoginInfo, Mt4order, WhiteList

from WestffsSchedules.utils.city_cut import get_city, user_city_cut
from WestffsSchedules.utils.mails import PySendMail
from WestffsSchedules.utils.origin_db import curl_conn, warning_emails

index_trade = ['100GBP', '200AUD', '225JPY', 'E35EUR', 'D30EUR', 'E50EUR', 'F40EUR', 'U30USD', 'S35EUR', 'H50HKD',
               'H33HKD', 'NASUSD']

real_group = ['W-03', 'W-03-Co-10', 'W-03-Co-20', 'W-03-STP', 'W-05', 'W-05-Co-10', 'W-05-Co-20', 'W-05-Co-20-STP',
              'W-05-STP', 'W-10', 'W-10-20', 'W-10-Co-10', 'W-10-Co-10-STP', 'W-10-Co-20', 'W-10-STP', 'W-20',
              'W-20-STP', 'W-20S', 'W-30', 'W-30-STP', 'W-30S', 'W-40', 'W-50', 'W-60', 'W-Co-03', 'W-Co-05',
              'W-Co-10', 'W-Co-10-STP', 'W-Co-20', 'W-Co-20-STP', 'W-Co-30', 'W-Co-30-STP', 'W-Co-40', 'W-Co-40-STP',
              'W-Co-50', 'W-Co-50-STP', 'W-Co-60', 'W-Co-60-STP', 'W-Default', 'W-Default-RC', 'W-Default-SP',
              'W-Default-STP', 'W-VIP', 'W-VIP-STP']

def method_test(logger):
    mailadd = warning_emails(logger)
    print(mailadd)


def url_request_resp(api, items, page, data, logger):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132'
                      ' Safari/537.36 QIHU 360SE'
    }
    url = r"http://47.75.192.61/api/Values/%s/%d/%d" % (api, items, page)

    logger.info("login_info url地址：%s" % url)
    try:
        resp = requests.get(url, headers=headers, params=data, timeout=(50, 100)).json()

    except():
        logger.error("get url data error")
        return ''
    # html_json = requests.get(url_login_info, timeout=(5, 10)).json()
    if api == "GetTradeRecord":
        return resp
    else:
        try:
            lines = resp.get('rows')
            if lines:
                return lines
            elif lines is None:
                logger.info("no data on this page")
                return ''
            else:
                logger.error("get json data error")

                ex = resp.get("ExceptionType")
                if ex:
                    logger.error("system error as %s and with api %s" % (ex, api))

                return ''
        except Exception as e:
            lines = ''
            logger.error("get json data error")
            return lines


def get_login_his(logger):
    startTime = endTime = date.today() - timedelta(days=1)
    page = 1
    payload = {'orderBy': '-id', 'startTime': startTime, 'endTime': endTime}
    api = 'GetLoginInfoLog'
    items = 100

    while True:
        lines = url_request_resp(api, items, page, payload, logger)
        page = page + 1
        if len(lines) == 0 or lines == '':
            break

        param = []
        for index in lines:
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

    return True


def get_login_last(logger):
    startData = endDate = date.today()
    ref_time = (datetime.datetime.now()-datetime.timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S')
    page = 1
    payload = {'startData': startData, 'endDate': endDate}
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
    title = u"注册地址与登陆地址不相符"
    warn_type = u"异地登陆预警"

    warned_accounts = []

    warn_accs = WarningLoginInfo.query.with_entities(WarningLoginInfo.account).all()

    if len(warn_accs) != 0:
        for item in warn_accs:
            warned_accounts.append(item.account)

    while True:
        lines = url_request_resp(api, items, page, payload, logger)
        if len(lines) == 0 or lines == '':
            break
        page = page + 1

        param = []
        for index in lines:

            words_list = get_city(index.get('City'))

            province = words_list[0]
            city_detail = words_list[1]
            # 查找异地登陆账号  当日登陆  非测试用户 该方法每小时执行，那么只需要对比每小时的账号即可

            # if int(index.get('LoginTime')[11:13]) - ref_hour <= 2:
            # if index.get('LoginTime')[:10] == datetime.date.today().strftime('%Y-%m-%d'):
            if index.get('LoginTime')[:19] > ref_time:

                account = index.get('Account')
                # warning_account = WarningLoginInfo.query.filter_by(account=account).first()
                #
                # if warning_account is not None:
                #
                #     print(warning_account)
                #     continue
                if account in warned_accounts:

                    continue

                mt4list = Mt4List.query.filter_by(account=account).first()

                if mt4list and mt4list.group_name not in ['W-SystemTest', 'W-Test']:

                    user_id = mt4list.user_id

                    userinfo = UserInfo.query.filter_by(user_id=user_id).first()

                    if userinfo and userinfo.province != province and userinfo.province != '':
                        userids.append(user_id)
                        usernames.append(userinfo.name)
                        address.append(userinfo.address)
                        accounts.append(account)
                        log_address.append(index.get("City"))
                        log_time.append(index.get("LoginTime"))

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

    if len(accounts) != 0:
        frame = pd.DataFrame(data)
        df_html = frame.to_html(escape=False)

        sendmail = PySendMail()
        ret = sendmail.mail(df_html, warn_type, title)
        if ret:
            print("邮件发送成功")
        else:
            logger.error("邮件发送失败, api %s" % warn_type)

        for i in range(len(accounts)):
            warning_info = WarningLoginInfo()
            warning_info.account = accounts[i-1]
            warning_info.city = address[i-1]

            warning_info.save()

    return ''


def clear_warning_form():

    # db.session.execute("delete from warning_login_info")
    # 不在白名单的将被删除
    WarningLoginInfo.query.filter_by(code=0).delete()
    db.session.commit()

    return 'delete'


def add_userinfo(logger):
    btime = date.today() - timedelta(days=7)
    etime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    page = 1
    payload = {'BeginTime': btime, 'EndTime': etime}
    api = 'GetUserInfo'
    items = 100

    while True:
        lines = url_request_resp(api, items, page, payload, logger)
        page = page + 1
        if len(lines) == 0 or lines == '':
            break

        for index in lines:
            # print(index)
            user_id = index.get('UserID')
            had_userinfo = UserInfo.query.filter_by(user_id=user_id).first()
            # print(had_userinfo)
            if had_userinfo:
                continue

            user = UserInfo()
            user.user_id = user_id
            user.name = index.get('UserName')
            user.name_cn = index.get('UserNameCn')
            user.birthday = index.get('Birthday').replace('T', ' ').split('.')[0] if index.get('Birthday') is not None else ''
            user.sex = index.get('Sex')
            user.address = index.get('Address')
            user.user_status = index.get('UserStatus')
            user.agent = index.get('Agent')
            user.ib = index.get('IB')
            user.level_id = index.get('LevelID')
            user.in_money = index.get('InMoney')
            user.user_money = index.get('UserMoney')
            user.create_time = index.get('CreateTime').replace('T', ' ').split('.')[0] if index.get('CreateTime') is not None else ''
            user.last_login_time = index.get('LastLoginTime').replace('T', ' ').split('.')[0] if index.get('LastLoginTime') is not None else ''
            user.intro_id = index.get('IntroID')
            user.employee_id = index.get('EmployeeID')
            user.is_trade_company = index.get('IsTradeCompany')
            user.is_office = index.get('IsOffice')

            words_list = user_city_cut(index.get('Address'))

            province = words_list[0]
            city_detail = words_list[1]

            user.province = province
            user.city = city_detail

            user.save()

    return 'success'


def add_mt4list(logger):
    btime = date.today() - timedelta(days=7)
    etime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    page = 1
    payload = {'BeginTime': btime, 'EndTime': etime}
    api = 'GetMt4List'
    items = 100

    while True:
        lines = url_request_resp(api, items, page, payload, logger)
        page = page + 1
        if len(lines) == 0 or lines == '':
            break

        for index in lines:
            # print(index)
            account = index.get('_Account')

            had_account = Mt4List.query.filter_by(account=account).first()
            # print(had_account)
            if had_account:
                had_account.in_money = index.get("InMoney")
                had_account.out_money = index.get("OutMoney")
                had_account.balance = index.get("Balance")
                had_account.margin = index.get("Margin")
                had_account.equity = index.get("Equity")
                had_account.profit = index.get("Profit")
                had_account.trade_fee = index.get("TradeFee")
                had_account.margin = index.get("Margin")

                had_account.save()
            else:
                mt4list = Mt4List()
                mt4list.account = account
                mt4list.user_id = index.get("UserID")
                mt4list.name = index.get("Mt4Name")
                mt4list.server_id = index.get("ServerID")
                mt4list.in_money = index.get("InMoney")
                mt4list.out_money = index.get("OutMoney")
                mt4list.balance = index.get("Balance")
                mt4list.margin = index.get("Margin")
                mt4list.equity = index.get("Equity")
                mt4list.profit = index.get("Profit")
                mt4list.group_name = index.get("GroupName")
                mt4list.leverage = index.get("Leverage")
                mt4list.trade_fee = index.get("TradeFee")
                mt4list.create_time = index.get("CreateTime") if index.get("CreateTime") is not None else ''
                mt4list.status = index.get("Status") if index.get("Status") is not None else 0
                mt4list.is_real = index.get("IsReal") if index.get("IsReal") is not None else 0
                mt4list.credit = index.get("Credit") if index.get("Credit") is not None else 0

                mt4list.save()

    return 'success'


# 通过账号获取该时间段内的订单记录
def get_mt4order(filelogger):
    etime = datetime.datetime.now().strftime("%Y-%m-%dT%H:00:00")
    btime = (datetime.datetime.now() - datetime.timedelta(hours=9)).strftime("%Y-%m-%dT%H:00:00")
    page = 1
    payload = {'BeginTime': btime, 'EndTime': etime}
    api = 'GetMt4Order'
    items = 100

    filelogger.info(api)

    while True:
        lines = url_request_resp(api, items, page, payload, filelogger)
        page = page + 1
        if len(lines) == 0 or lines == '':
            break

        for index in lines:
            # 查看是否已经有记录
            order = index.get('Mt4Order')
            had_order = Mt4order.query.filter_by(mt4_order=order).first()

            if had_order:
                continue

            # 如果有balance交易则更新出入金
            if index.get('Cmd') == "Balance":
                mt4list = Mt4List.query.filter_by(account=index.get('Account')).first()
                info = url_request_resp(api='GetMt4List', items=1, page=1, data={"Account": index.get('Account')}, logger=filelogger)
                for item in info:
                    mt4list.in_money = item.get("InMoney")
                    mt4list.out_money = item.get("OutMoney")
                    mt4list.balance = item.get("Balance")
                    mt4list.equity = item.get("Equity")
                    mt4list.profit = item.get("Profit")
                    mt4list.trade_fee = item.get("TradeFee")
                    mt4list.save()

            for i in index.keys():
                if index[i] is None:
                    index[i] = ''
                else:
                    if i in ['OpenTime', 'CloseTime']:
                        index[i] = index[i].replace('T', ' ')

            mt4Order = Mt4order()
            mt4Order.account = index.get("Account")
            mt4Order.mt4_order = order
            mt4Order.cmd = index.get("Cmd")
            mt4Order.symbol = index.get("Symbol")
            mt4Order.open_price = index.get("OpenPrice")
            mt4Order.close_price = index.get("ClosePrice")
            mt4Order.profit = index.get("Profit")
            mt4Order.volume = index.get("Volume")
            mt4Order.open_time = index.get("OpenTime")
            mt4Order.close_time = index.get("CloseTime")
            mt4Order.server_id = index.get("ServerID")
            mt4Order.userId = index.get("UserID")
            mt4Order.trust_in_money = index.get("TrustInMoney")
            mt4Order.night_interest = index.get("NightInterest")
            mt4Order.sl = index.get("SL")
            mt4Order.tp = index.get("TP")
            mt4Order.commission = index.get("Commission")

            mt4Order.save()
    return 'success'


# 获取持仓单记录
def get_trade_order(filelogger):
    key = '69668E9A346744D27E7B36FD4C30DE56'
    page = 1
    payload = {'key': key}
    api = 'GetTradeRecord'
    items = 100
    filelogger.info(api)
    paras = []

    # 存放订单号
    orders = []
    # 存放指数报警
    warning_index_order = []
    warning_index_account = []
    warning_index_symbol = []
    warning_index_lots = []
    warning_index = {
        'warning_index_order': warning_index_order,
        'warning_index_account': warning_index_account,
        'warning_index_symbol': warning_index_symbol,
        'warning_index_lots': warning_index_lots,
    }
    # 存放手数报警
    warning_lots_order = []
    warning_lots_account = []
    warning_lots_symbol = []
    warning_lots_lots = []
    warning_lots = {
        'warning_lots_order': warning_lots_order,
        'warning_lots_account': warning_lots_account,
        'warning_lots_symbol': warning_lots_symbol,
        'warning_lots_lots': warning_lots_lots,
    }
    stime = int(time.time())
    lines = url_request_resp(api, items, page, payload, filelogger)
    nowtime = int(time.time())
    filelogger.info("trade download time is %d" % (nowtime-stime))
    for index in lines:

        if nowtime - index.get('OpenTime') < 15:
            if index.get("Symbol") in index_trade:
                check_white_act = WhiteList.query.filter_by(account=index.get('Login')).first()
                if not check_white_act:
                    warning_index_order.append(index.get('Order'))
                    warning_index_account.append(index.get('Login'))
                    warning_index_symbol.append(index.get('Symbol'))
                    warning_index_lots.append(index.get('Volume')/100)

            if index.get('Volume') >= 500:
                print(index.get('Login'))
                check_white_act = WhiteList.query.filter_by(account=index.get('Login')).first()
                if not check_white_act:
                    warning_lots_order.append(index.get('Order'))
                    warning_lots_account.append(index.get('Login'))
                    warning_lots_symbol.append(index.get('Symbol'))
                    warning_lots_lots.append(index.get('Volume')/100)
        orders.append(str(index.get('Order')))
        para = "(%d,%d,'%s',%d,%d,%d,%d,%d,%f,%f,%f,%d,%d,%d,%f,%f,%f,%f,%f,%f,%d,'%s',%d,%f,%d)" % \
               (index.get('Order'), index.get('Login'), index.get('Symbol'), index.get('Digits'), index.get('Cmd'),
                index.get('Volume'), index.get('OpenTime'), index.get('State'), index.get('OpenPrice'), index.get('Sl'),
                index.get('Tp'), index.get('CloseTime'), index.get('Expiration'), index.get('Reason'),
                index.get('Commission'), index.get('CommissionAgent'), index.get('Storage'), index.get('ClosePrice'),
                index.get('Profit'), index.get('Taxes'), index.get('Magic'), index.get('Comment'),
                index.get('Activation'), index.get('MarginRate'), index.get('Timestamp'))
        paras.append(para)

    params = ','.join(paras)

    # 获取上一个时间点的订单号
    last_orders = []
    get_last_order_Sql = "Select `Order` from tradeorder;"
    res = db.session.execute(get_last_order_Sql)
    for i in res:
        last_orders.append(str(i[0]))
    last_orders = set(last_orders)
    new_orders = set(orders)

    # 获取平仓单订单号
    close_orders = last_orders - (last_orders & new_orders)

    # # closeorder(close_orders, "closeorder", cur, conn)
    if len(close_orders) > 0:
        accounts = ','.join(close_orders)
        # 删除平仓数据

        delete_close_order_Sql = 'DELETE FROM tradeorder where `order` in (%s);' % accounts

        db.session.execute(delete_close_order_Sql)
        db.session.commit()

    # 插入持仓单
    Sql = "replace into TradeOrder(`order`,account,symbol,digits,cmd,volume,open_time,state,open_price,sl,tp," \
          "close_time,expiration,reason,commission,commission_agent,storage,close_price,profit,taxes,magic,comment," \
          "activation,margin_rate,timestamp) values %s" % params

    curl_conn(sql=Sql, api="insert_tradeorder_sql", logger=filelogger)
    # 更新头寸
    delete_cmd_SQL = "DELETE FROM `trade_symbol_index` WHERE CONCAT(symbol,cmd) not in (SELECT CONCAT(symbol,IF" \
                     "(cmd=0,'Buy','Sell')) FROM tradeorder WHERE cmd in (0,1) GROUP BY symbol,cmd);"
    curl_conn(sql=delete_cmd_SQL, api="delete_cmd_sql", logger=filelogger)
    insert_cmd_SQL = "REPLACE INTO `trade_symbol_index` (SELECT symbol,IF(cmd=0,'Buy','Sell'), COUNT(*), " \
                     "SUM(volume)*0.01, SUM(profit) FROM `tradeorder` WHERE cmd in (0,1) GROUP BY symbol,cmd)"
    curl_conn(sql=insert_cmd_SQL, api="insert_cmd_SQL", logger=filelogger)

    # print(datetime.datetime.now())
    if len(warning_index_order) != 0:
        frame = pd.DataFrame(warning_index)
        df_html = frame.to_html(escape=False)

        title = u"进行指数交易订单"
        warn_type = u"指数订单预警"

        sendmail = PySendMail()
        ret = sendmail.mail(df_html, warn_type, title)
        if ret:
            print("邮件发送成功")
        else:
            filelogger.error("邮件发送失败, api %s" % warn_type)

    if len(warning_lots_order) != 0:
        filelogger.info(warning_lots)
        frame = pd.DataFrame(warning_lots)
        df_html = frame.to_html(escape=False)

        title = u"单次交易手数大于5"
        warn_type = u"手数过大订单预警"

        sendmail = PySendMail()
        ret = sendmail.mail(df_html, warn_type, title)
        if ret:
            print("邮件发送成功")
        else:
            filelogger.error("邮件发送失败, api %s" % warn_type)

    return
