# _*_ coding: UTF-8 _*_
# 开发团队  : 宽粉汇科
# 开发人员  : LianXiaoRui
# 开发时间  : 2019/11/6 16:38
# 文件名称  : logger.py
# 开发工具  : PyCharm
# 项目名称  : aspschedule
import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler


def add_file_logger(app):
    handler = TimedRotatingFileHandler(app.config['LOG_FILE_PATH'], 'D', 1, 7, None, False, False)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'))
    app.logger.addHandler(handler)


# 创建一个普通logger
def get_logger():
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)


    # # 创建一个handler，用于写入日志文件
    # fh = logging.FileHandler('tradeorder.log')
    # fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件, 定期清理日志
    log_file_handler = logging.handlers.TimedRotatingFileHandler(filename="westffs.log", when="D", interval=1, backupCount=5)
    log_file_handler.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    log_file_handler.setFormatter(formatter)

    # 给logger添加handler
    # logger.addHandler(fh)
    logger.addHandler(ch)
    logger.addHandler(log_file_handler)

    return logger


def schedule_logger():
    LOGGER_CONFIG = {
        'version': 1,
        'formatters': {
            'simple': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
            # 其他的 formatter
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'simple'
            },
            'file': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': './logs/Westfield_logging.log',
                'encoding': 'utf-8',
                'level': 'DEBUG',
                'formatter': 'simple',
                'when': 'D',
                'interval': 1,
                'backupCount': 5,
            },
            # 其他的 handler
        },
        'loggers': {
            'StreamLogger': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
            'FileLogger': {
                # 既有 console Handler，还有 file Handler
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
            },
            # 其他的 Logger
        }
    }

    logging.config.dictConfig(LOGGER_CONFIG)
    filelogger = logging.getLogger("FileLogger")

    return filelogger