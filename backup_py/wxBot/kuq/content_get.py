from config.config import KQ_TIME, KUQ_DATA_PATH, CX_MIN, ELEME_DATA_PATH, ID_MAX, USER, PWD, HOST
from config.fangtang import fangtang
from eleme.hongbao.hongbao_jk_fqq import jk_fqq_hongbao
from kuq.content_cx import cx_content
# from hongbao.hongbao_xh import xh_hongbao
import sqlite3
import logging.handlers
import threading
import inspect
import ctypes
import traceback
import datetime
import time, requests, re
from daka_warn.send_daka import send_daka_index
from eleme.sign.send_sign import send_sign_index
import pymysql
from apscheduler.schedulers.blocking import BlockingScheduler

class my_thread(threading.Thread):
    def __init__(self, bianhao, group_sn, alink, group, dahao, hz_group, logger, uid):
        threading.Thread.__init__(self)
        self.th_id = bianhao
        self.group_sn = group_sn
        self.alink = alink
        self.group = group
        self.dahao = dahao
        self.hz_group = hz_group
        self.logger = logger
        self.uid = uid
    def run(self):
        jk_fqq_hongbao(self.group_sn, self.th_id, self.alink, self.group, self.dahao, self.hz_group, self.logger, self.uid, True)
def index(bianhao, group_sn, alink, group, dahao, hz_group, logger, uid):
    th = my_thread(bianhao, group_sn, alink, group, dahao, hz_group, logger, uid)  # id, name
    th.start()
    th.setName('hongbao{}'.format(bianhao))

LOG_FILE = r'log\eleme_qq.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 实例化handler
fmt = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter
logger = logging.getLogger('eleme_qq')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)


uid = 1
x = 0

#获取酷Q接收的聊天记录 从中筛选出饿了么红包消息 加入红包监控
def content(bot, ticks, is_jianK):
    global x, uid
    mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306,
                                 db='eleme')
    mysql_cursor = mysql_conn.cursor()  # 获取游标
    kq_conn = sqlite3.connect(KUQ_DATA_PATH)  # 酷Q聊天信息库地址
    kq_cursor = kq_conn.cursor()  # 获取游标
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    # logger.info('开始查询')
    # 打卡提醒服务
    week_int = datetime.datetime.now().weekday()
    sign_time = datetime.datetime.now().strftime('%H:%M')
    if week_int != 5 and week_int != 6: # 周末不提醒，5代表星期六
        # 该方法是异步执行
        send_daka_index(bot)
    if sign_time == '09:00':
        # logger.info('开始执行饿了么签到')
        send_sign_index(bot, logger)
        # logger.info('饿了么签到调用成功')

    tup = cx_content(kq_cursor, ticks)
    num = tup[1]  # 共获取到多少条聊天记录
    contents = tup[0]  # 聊天记录 数组里包元组格式
    # 该判断为每次未获取到新消息时就不进行聊天记录循环
    if num > x:
        hbUrlList = []
        hbNumList = []
        i = num - x
        # 只对新消息进行循环，旧记录忽略
        for c in range(1, i + 1):
            content = contents[-c][0]
            # print('消息 --》',content)
            # 判断是否为饿了么红包
            if '饿了么拼手气，第' in content or '【饿了么】第' in content:
                hongbaoMax = int(re.findall('第(.*?)个', content)[0])
                if '"jumpUrl"' in content:
                    uurls = re.findall('"jumpUrl":"(.*?)"', content)
                    if len(uurls) != 0:
                        if 'http' in uurls[0]:
                            url = 'url={},'.format(uurls[0])
                        else:
                            url = 'url=https://{},'.format(uurls[0])
                        hbUrlList.append(url)
                        hbNumList.append(hongbaoMax)
                    else:
                        logger.info('匹配出错，{}'.format(content))
                else:
                    hbUrlList.append(content)
                    hbNumList.append(hongbaoMax)
            elif '-!饿了么签到!-' == content:
                send_sign_index(bot, logger)
                logger.info('通过指令开启饿么了签到~')
        if len(hbUrlList) != 0:
            for u in range(len(hbUrlList)):
                try:
                    cursor.execute('''select count from eleme_count WHERE id = 1 ''')  # 查找饿了么库
                    bianhao = int(cursor.fetchall()[0][0])
                    urls = re.findall('url=(.*?),', hbUrlList[u])
                    if len(urls) != 0:
                        url = urls[0]
                        #判断是否为短网址
                        if 'url.cn' in url:
                            # 获取到的url为短网址格式，下面进行还原
                            r = requests.post(
                                'https://duanwangzhihuanyuan.51240.com/web_system/51240_com_www/system/file/duanwangzhihuanyuan/get/?ajaxtimestamp=1556095865699',
                                data={'turl': url})
                            if r.status_code == 200:
                                # 还原成功后再匹配sn码
                                alink = re.findall('<a href="(.*?)"', r.text, re.S)[0]
                                group_sn = re.findall('sn=(.*?)&', alink)[0]
                                logger.info('已捕获到饿了么红包sn[{}],标记为【红包{}】'.format(group_sn, bianhao))
                                # 拿到sn码调用到红包监控方法（该方法为异步执行）
                                if is_jianK:
                                    # jk_fqq_hongbao(group_sn, bianhao, alink, group, logger)

                                    mysql_cursor.execute(
                                        "INSERT INTO eleme_group_sn (bianhao, group_sn, yet, yet_max, alink, state, wx_beizhu, add_times) VALUES ('{}', '{}', 0, {}, '{}', 'yes', '红包互助群', '{}')".format(
                                            bianhao, group_sn, hbNumList[u],
                                            alink, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                    )
                                    mysql_conn.commit()

                                    # index(bianhao, group_sn, alink, group, dahao, hz_group, logger, uid)
                                    # if uid == ID_MAX:
                                    #     uid = 1
                                    # else:
                                    #     uid += 1
                                else:
                                    # xh_hongbao(group_sn, bianhao, alink)
                                    pass
                                bianhao += 1
                                cursor.execute(
                                    '''UPDATE eleme_count SET count = '{}' WHERE id = 1'''.format(bianhao))  # 查找饿了么库
                                conn.commit()
                            else:
                                logger.info('短网址还原出错~', r.status_code, r.text)
                        else:
                            alink = url
                            group_sn = re.findall('sn=(.*?)&', alink)[0]
                            logger.info('已捕获到饿了么红包sn[{}],标记为【红包{}】'.format(group_sn, bianhao))
                            # 拿到sn码调用到红包监控方法（该方法为异步执行）
                            if is_jianK:

                                mysql_cursor.execute(
                                    "INSERT INTO eleme_group_sn (bianhao, group_sn, yet, yet_max, alink, state, wx_beizhu, add_times) VALUES ('{}', '{}', 0, {}, '{}', 'no', '红包互助群', '{}')".format(
                                        bianhao, group_sn, hbNumList[u],
                                        alink, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                                )
                                mysql_conn.commit()

                                # index(bianhao, group_sn, alink, group, dahao, hz_group, logger, uid)
                                # if uid == ID_MAX:
                                #     uid = 1
                                # else:
                                #     uid += 1
                            else:
                                # xh_hongbao(group_sn, bianhao, alink)
                                pass
                            bianhao += 1
                            cursor.execute(
                                '''UPDATE eleme_count SET count = '{}' WHERE id = 1'''.format(bianhao))  # 查找饿了么库
                            conn.commit()
                    else:
                        logger.debug('{},匹配sn出错了~'.format(hbUrlList[u]))
                except:
                    print(traceback.format_exc())
                    logger.debug('{},提取sn出错了~ {}'.format(hbUrlList[u], traceback.format_exc()))
                if len(hbUrlList) > 1:
                    time.sleep(3)
        x = num
    # logger.info('等待了60秒')
    # group.send('本群大红包推送已关闭')
    # fangtang('饿了么大包', '饿了么大包群大红包推送已关闭')

def get_content(is_jianK, bot):
    # 2020.1.16去除3个参数 group, dahao, hz_group

    fangtang('饿了么大包', '饿了么大包群已开启大红包推送，请记得留意群消息')
    print('指令执行成功，监控系统运行中...')
    # group.send('本群已开启大红包推送，请记得留意群消息')
    ticks = int(time.time()) #获取运行该脚本时的时间戳
    otherStyleTime = time.strftime("%H:%M:%S", time.localtime(ticks - CX_MIN * 60))
    logger.info(
        '酷Q消息监控中,每隔{}秒查询一次记录{}~'.format(KQ_TIME, '' if CX_MIN == 0 else ',本次查找了{}之后的记录'.format(otherStyleTime)))
    content(bot, ticks, is_jianK)
    scheduler = BlockingScheduler()
    # hours=2 每2时执行一次 minutes=1 每1分钟执行一次 seconds=3 每3秒钟执行一次
    scheduler.add_job(lambda: content(bot, ticks, is_jianK), 'interval', minutes=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print('定时任务出现异常')

def wxGroup_jk(bianhao, group_sn, alink, group, dahao, hz_group, uid):
    logger.info('wxGroup - 已捕获到饿了么红包sn[{}],标记为【红包{}】'.format(group_sn, bianhao))
    index(bianhao, group_sn, alink, group, dahao, hz_group, logger, uid)
    conn = sqlite3.connect(ELEME_DATA_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    bianhao += 1
    cursor.execute(
        '''UPDATE eleme_count SET count = '{}' WHERE id = 1'''.format(bianhao))  # 查找饿了么库
    conn.commit()
def ins_stop():
    kq_conn1 = sqlite3.connect(KUQ_DATA_PATH)  # 酷Q聊天信息库地址
    kq_cursor1 = kq_conn1.cursor()  # 获取游标
    s = int(time.time())
    kq_cursor1.execute("INSERT INTO event (content, time) VALUES ('-!停止监控!-', '{}')".format(s))
    kq_conn1.commit()
    # print('插入指令成功')

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_jk():
    # print('当前: ', threading.enumerate()) #返回一个包含正在运行的线程的list
    lists = threading.enumerate()
    for i in range(1, len(lists)):
        if 'hongbao' in lists[i].name:
            _async_raise(lists[i].ident, SystemExit)
        # print('关闭了线程名: ', lists[i].name)  # 返回一个包含正在运行的线程的list
        # time.sleep(5)
        # print('现在: ', threading.enumerate())  # 返回一个包含正在运行的线程的list
    # print('最后: ', threading.enumerate()) #返回一个包含正在运行的线程的list

def get_hbnum_fqq():
    hbList = threading.enumerate()
    hbNameList = []
    for hb in hbList:
        if 'hongbao' in hb.name:
            hbNameList.append(hb.name)
    return hbNameList