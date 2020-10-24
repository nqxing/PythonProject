import logging.handlers
import traceback
from random import randint
from plugins.pub_fun.sql_all import MysqlSearch as SQL

LOG_FILE = r'mirai.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=5120 * 5120, backupCount=5,
                                               encoding='utf-8')  # 实例化handler
fmt = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter
logger = logging.getLogger('mirai')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)


def write_log(level, text):
    if level == 1:
        logger.info(text)
    elif level == 2:
        logger.debug(text)
    else:
        logger.error(text)