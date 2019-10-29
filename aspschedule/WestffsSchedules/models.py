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

    Id = db.Column(db.Integer, primary_key=True, autoincrement=False, name='id')

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

    # id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    Account = db.Column(db.Integer, nullable=False, name='account')
    Ip = db.Column(db.String(16), nullable=False, name='ip')
    Address = db.Column(db.String(128), nullable=False, name='address')
    City = db.Column(db.String(64), nullable=False, name='city')
    LoginTime = db.Column(db.DateTime, nullable=False, name='login_time')
    LeaveTime = db.Column(db.DateTime, nullable=False, name='leave_time')
    OnlineMinute = db.Column(db.Integer, nullable=False, name='online_minute')
    province = db.Column(db.String(64), nullable=False, default='')
    city_name = db.Column(db.String(64), nullable=False, default='')

