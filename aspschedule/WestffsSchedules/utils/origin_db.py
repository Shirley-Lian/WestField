# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/11/15 18:09
# 文件名称  : origin_db.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
from WestffsSchedules.ext import db


def curl_conn(sql, api, logger):
    try:
        db.session.execute(sql)
        db.session.commit()
    except Exception as e:
        logger.error("the api %s run error as %s" % (api, e))


def warning_emails(logger):
    sql = "select email from warning_emails;"
    emails = []
    try:
        res = db.session.execute(sql)
        for email in res:
            emails.append(email[0])
        if len(emails) == 1:
            index = ''
            emails.append(index)
        return emails
    except Exception as e:
        logger.error("the api %s run error as %s" % ("warning_emails", e))
