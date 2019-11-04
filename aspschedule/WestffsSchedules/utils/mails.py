# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/30 15:13
# 文件名称  : mails.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
# coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import pandas as pd

import datetime

from WestffsSchedules.settings import Config

pd.set_option('display.max_colwidth', -1) # 设置表格数据完全显示（不出现省略号）

#
# def get_account():
#     SQL = "SELECT u.user_id as UserID, u.user_name as UserName, u.address as `注册地址`, l.account as `登陆账号`, " \
#           "l.city as `登陆地址`, l.login_time as `最后一次登陆时间` FROM `userinfo` u LEFT JOIN mt4list m on " \
#           "u.user_id = m.user_id LEFT JOIN login_lastinfo l on m.account = l.account WHERE u.address != '' " \
#           "and u.address != '0' AND u.province != l.province and m.group_name not in ('W-SystemTest', 'W-Test') " \
#           "AND YEAR(l.login_time) > 2018 AND LOCATE('Test',u.user_name) = 0 AND LOCATE('est_',u.user_name) = 0 " \
#           "ORDER BY l.login_time;"
#     try:
#         df = pd.read_sql_query(SQL, engine)
#         return df
#     except Exception as e:
#         print(e)
#         print("get account error")


class PySendMail:

    body = \
        """
        <body>

        <div align="center" class="header">
            <!--标题部分的信息-->
            <h1 align="center">{titles}</h1>
            <h2 align="center">{yesterday}</h2>
        </div>

        <hr>

        <div class="content">
            <!--正文内容-->
            <h2> </h2>

            <div>
                <h4></h4>
                {df_html}

            </div>
            <hr>

            <p style="text-align: center">

            </p>
        </div>
        </body>
        """  # .format(yesterday=get_yesterday(),df_html=df_html)

    head = \
        """
        <head>
            <meta charset="utf-8">
            <STYLE TYPE="text/css" MEDIA=screen>

                table.dataframe {
                    border-collapse: collapse;
                    border: 2px solid #a19da2;
                    /*居中显示整个表格*/
                    margin: auto;
                }

                table.dataframe thead {
                    border: 2px solid #91c6e1;
                    background: #f1f1f1;
                    padding: 10px 10px 10px 10px;
                    color: #333333;
                }

                table.dataframe tbody {
                    border: 2px solid #91c6e1;
                    padding: 10px 10px 10px 10px;
                }

                table.dataframe tr {

                }

                table.dataframe th {
                    vertical-align: top;
                    font-size: 14px;
                    padding: 10px 10px 10px 10px;
                    color: #105de3;
                    font-family: arial;
                    text-align: center;
                }

                table.dataframe td {
                    text-align: center;
                    padding: 10px 10px 10px 10px;
                }

                body {
                    font-family: 宋体;
                }

                h1 {
                    color: #5db446
                }

                div.header h2 {
                    color: #0002e3;
                    font-family: 黑体;
                }

                div.content h2 {
                    text-align: center;
                    font-size: 28px;
                    text-shadow: 2px 2px 1px #de4040;
                    color: #fff;
                    font-weight: bold;
                    background-color: #008eb7;
                    line-height: 1.5;
                    margin: 20px 0;
                    box-shadow: 10px 10px 5px #888888;
                    border-radius: 5px;
                }

                h3 {
                    font-size: 22px;
                    background-color: rgba(0, 2, 227, 0.71);
                    text-shadow: 2px 2px 1px #de4040;
                    color: rgba(239, 241, 234, 0.99);
                    line-height: 1.5;
                }

                h4 {
                    color: #e10092;
                    font-family: 楷体;
                    font-size: 20px;
                    text-align: center;
                }

                td img {
                    /*width: 60px;*/
                    max-width: 300px;
                    max-height: 300px;
                }

            </STYLE>
        
        </head>
        """

    def __init__(self):
        self.my_sender = Config.MAIL_USERNAME  # 发件人邮箱账号
        self.my_pass = Config.MAIL_PASSWORD  # 发件人邮箱密码
        self.server_smtp = Config.MAIL_SERVER # SMTP服务器地址
        self.server_port = Config.MAIL_PORT

    def mail(self, df_html, user, warning_type, title):
        ret = True
        body = self.body.format(titles=title, yesterday=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), df_html=df_html)
        html_msg = "<html>" + self.head + body + "</html>"
        html_msg = html_msg.replace('\n', '').encode("utf-8")
        my_user = user  # 收件人邮箱账号，我这边发送给自己
        # try:
        msg = MIMEText(html_msg, 'html', 'utf-8')
        msg['From'] = formataddr(["QuantFintech", self.my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        # msg['To'] = formataddr(["Harry", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = ','.join(my_user)
        # msg['To'] = ','.join(formataddr(["Harry", my_user]))
        msg['Subject'] = "【westfield】" + warning_type # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL(self.server_smtp, self.server_port)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(self.my_sender, self.my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(self.my_sender, msg['To'].split(','), msg.as_string().encode('utf-8'))  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        # except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        #     ret = False
        #     print(e)
        return ret
#
# # 获取数据
# filter_merge_data = ''
# df_html = filter_merge_data.to_html(escape=False) #DataFrame数据转化为HTML表格形式
#
# # warn_type = "订单预警"
# title = "注册地址与登陆地址不相符"
# warn_type = "异地登陆预警"
# # mailadd = "zhangh0725@gmail.com"
# # mailadd = "lianxiaorui0511@163.com"
# mailadd = "dofuy007@gmail.com"
# sendmail = PySendMail()
# ret = sendmail.mail(df_html, mailadd, warn_type, title)
# if ret:
#     print("邮件发送成功")
# else:
#     print("邮件发送失败")