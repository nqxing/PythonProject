import logging.handlers

INFO_LOG_FILE = r'log/info.log'
handler_info = logging.handlers.RotatingFileHandler(INFO_LOG_FILE, maxBytes=1024 * 1024, backupCount=5,
                                               encoding='utf-8')  # 实例化handler
fmt_info = '%(asctime)s - %(levelname)s - %(message)s'
formatter_info = logging.Formatter(fmt_info)  # 实例化formatter
handler_info.setFormatter(formatter_info)  # 为handler添加formatter
logger_info = logging.getLogger('wxPublic_info')  # 获取名为tst的logger
logger_info.addHandler(handler_info)  # 为logger添加handler
logger_info.setLevel(logging.DEBUG)

ERROR_LOG_FILE = r'log/error.log'
handler_error = logging.handlers.RotatingFileHandler(ERROR_LOG_FILE, maxBytes=1024 * 1024, backupCount=5,
                                               encoding='utf-8')  # 实例化handler
fmt_error = '%(asctime)s - %(levelname)s - %(message)s'
formatter_error = logging.Formatter(fmt_error)  # 实例化formatter
handler_error.setFormatter(formatter_error)  # 为handler添加formatter
logger_error = logging.getLogger('wxPublic_error')  # 获取名为tst的logger
logger_error.addHandler(handler_error)  # 为logger添加handler
logger_error.setLevel(logging.DEBUG)

def log(level, text):
    if level == 1:
        logger_info.info(text)
    elif level == 2:
        logger_error.debug(text)
    else:
        logger_error.error(text)