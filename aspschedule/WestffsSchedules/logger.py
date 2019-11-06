# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/11/6 16:38
# 文件名称  : logger.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
import logging
from logging.handlers import TimedRotatingFileHandler


def add_file_logger(app):
    handler = TimedRotatingFileHandler(app.config['LOG_FILE_PATH'], 'D', 1, 7, None, False, False)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'))
    app.logger.addHandler(handler)