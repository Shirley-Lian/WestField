# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/10/10 15:20
# 文件名称  : models.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
from WestffsSchedules.ext import db


class BaseModel(db.Model):
    __abstract__ = True

    # Id = db.Column(db.Integer, primary_key=True, autoincrement=False, name='id')

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

            return True
        except Exception as e:
            print(e)
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return True

        except Exception as e:

            print(e)

            return False


class LoginInfo(BaseModel):

    __tablename__ = 'login_info_log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    Account = db.Column(db.Integer, nullable=False, name='account')
    Ip = db.Column(db.String(16), nullable=False, name='ip')
    Address = db.Column(db.String(128), nullable=False, name='address')
    City = db.Column(db.String(64), nullable=False, name='city')
    LoginTime = db.Column(db.DateTime, nullable=False, name='login_time')
    LeaveTime = db.Column(db.DateTime, nullable=False, name='leave_time')
    OnlineMinute = db.Column(db.Integer, nullable=False, name='online_minute')
    province = db.Column(db.String(64), nullable=False, default='')
    city_name = db.Column(db.String(64), nullable=False, default='')


class TestModel(BaseModel):

    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(64))


class Mt4List(BaseModel):

    __tablename__ = 'mt4list'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.Integer, nullable=False, name='account')
    user_id = db.Column(db.Integer, nullable=False, name='user_id')
    name = db.Column(db.String(64), nullable=False, name='mt4_name')
    server_id = db.Column(db.Integer, nullable=False, name='server_id')
    in_money = db.Column(db.Float, nullable=False, name='in_money')
    out_money = db.Column(db.Float, nullable=False, name='out_money')
    balance = db.Column(db.Float, nullable=False, name='balance')
    margin = db.Column(db.Float, nullable=False, name='margin')
    equity = db.Column(db.Float, nullable=False, name='equity')
    profit = db.Column(db.Float, nullable=False, name='profit')
    group_name = db.Column(db.String(64), nullable=False)
    leverage = db.Column(db.Integer, nullable=False, name='leverage')
    trade_fee = db.Column(db.Float, nullable=False, name='trade_fee')
    create_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False, name='status')
    is_real = db.Column(db.Integer, nullable=False, name='is_real')
    credit = db.Column(db.Float, nullable=False, name='credit', default=0)


class UserInfo(BaseModel):

    __tablename__ = 'userinfo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False, name='user_id')
    name = db.Column(db.String(64), nullable=False, name='user_name')
    name_cn = db.Column(db.String(64), nullable=False, name='user_name_cn')
    birthday = db.Column(db.String(64), nullable=False, name='birthday')
    sex = db.Column(db.Integer, nullable=False, name='sex')
    address = db.Column(db.Integer, nullable=False, name='address', default='')
    user_status = db.Column(db.Integer, nullable=False, name='user_status')
    agent = db.Column(db.Integer, nullable=False, name='agent')
    ib = db.Column(db.Integer, nullable=False, name='ib')
    level_id = db.Column(db.Float, nullable=False, name='level_id')
    in_money = db.Column(db.Float, nullable=False, name='in_money')
    user_money = db.Column(db.Float, nullable=False, name='user_money')
    create_time = db.Column(db.String(64), nullable=False)
    last_login_time = db.Column(db.String(64), nullable=False)
    intro_id = db.Column(db.Integer, nullable=False, name='intro_id')
    employee_id = db.Column(db.Integer, nullable=False, name='employee_id')
    is_trade_company = db.Column(db.Integer, nullable=False, name='is_trade_company')
    is_office = db.Column(db.Integer, nullable=False, name='is_office')
    province = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)


class WarningLoginInfo(BaseModel):

    __tablename__ = 'warning_login_info'

    account = db.Column(db.Integer, primary_key=True, autoincrement=False, name='account')
    city = db.Column(db.String(128), nullable=False, name='city')
    code = db.Column(db.Integer, nullable=False, name='code', default=0)


class Mt4order(BaseModel):

    __tablename__ = 'mt4order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.Integer, nullable=False, name='account')
    user_id = db.Column(db.Integer, nullable=False, name='user_id')
    name = db.Column(db.String(64), nullable=False, name='mt4_name')
    server_id = db.Column(db.Integer, nullable=False, name='server_id')
    in_money = db.Column(db.Float, nullable=False, name='in_money')
    out_money = db.Column(db.Float, nullable=False, name='out_money')
    balance = db.Column(db.Float, nullable=False, name='balance')
    margin = db.Column(db.Float, nullable=False, name='margin')
    equity = db.Column(db.Float, nullable=False, name='equity')
    profit = db.Column(db.Float, nullable=False, name='profit')
    group_name = db.Column(db.String(64), nullable=False)
    leverage = db.Column(db.Integer, nullable=False, name='leverage')
    trade_fee = db.Column(db.Float, nullable=False, name='trade_fee')
    create_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False, name='status')
    is_real = db.Column(db.Integer, nullable=False, name='is_real')
    credit = db.Column(db.Float, nullable=False, name='credit', default=0)


