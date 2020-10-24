import requests
from pyquery import PyQuery as pq
# 禁用安全请求警告 关闭SSL验证时用
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re, time, datetime
from random import randint  # 随机函数
import random, string
import traceback
import threading

headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36'
        }

class dzReply(object):
    def __init__(self, bbs_dict):
        self.bbs_dict = bbs_dict
        self.headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
            'cookie': self.bbs_dict['cookie']
        }

    def reply(self, tid, message):
        url = "{}/forum.php?mod=post&action=reply&fid={}&tid={}&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1&file=&message={}&posttime={}&formhash={}&usesig=1&subject=++".\
            format(self.bbs_dict['host'], self.bbs_dict['fid'], tid, message, int(time.time()), self.bbs_dict['formhash'])
        try:
            r = requests.post(url, headers=self.headers, verify=False)
            # 抱歉，您所在的用户组每小时限制发回帖 30 个，请稍候再发表
            # 非常感谢，回复发布成功，现在将转入主题页，请稍候……[ 点击这里转入主题列表 ]
            # 抱歉，验证码填写错误
            # 抱歉，您两次发表间隔少于 50 秒，请稍候再发表
            # 回复需要审核，请等待通过，审帖时间为:8:30-12:00，14:00-18:00，19:30-21:00
            if '非常感谢，回复发布成功' in r.text:
                return 0
            else:
                with open('error.txt', 'a', encoding='utf-8') as f:
                    f.write('{} - 【回帖异常】 - {}\n---------------------------------------------\n'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), r.text))
                return r.text
        except:
            return -1

    def get_tid(self):
        num = 1
        stop_num = 0
        cep_num = 0
        start_time = None
        start_state = True #每小时首次回帖状态
        stop_state = False #金币值上限状态
        sleep_state = False #每小时回帖限制状态
        run_name = '[{}_{}]'.format(self.bbs_dict['bbs_name'], self.bbs_dict['user_name'])
        jinb = self.get_jinbi()
        gStr = '-----{}任务开始，起始{}为{}-----'.format(run_name, self.bbs_dict['jinb_name'], jinb)
        sava_txt(gStr)
        for i in range(randint(10, self.bbs_dict['page_max']), 0, -1):
            r = requests.get('{}{}'.format(self.bbs_dict['host'], self.bbs_dict['fid_url'].format(self.bbs_dict['fid'], i)), verify=False)
            html = pq(r.text)
            lis = html('#waterfall li').items()
            for li in lis:
                href = li('.cl a').attr('href')
                title = li('.cl a').attr('title')
                if self.bbs_dict['tid_split']:
                    tid = href.split('-')[1]
                else:
                    tid = re.findall("&tid=(.*?)&", href)[0]
                reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
                message = re.sub(reg, '', title)
                suij = self.suiji_uid()
                message = suij+message
                value = self.reply(tid, message)
                if value == 0:
                    if start_state:
                        start_time = int(time.time())
                        start_state = False
                    new_jinb = self.get_jinbi()
                    if new_jinb == jinb:
                        stop_num += 1
                    else:
                        jinb = new_jinb
                    gStr = '{} {} {} 第{}页 金币{} 回帖成功'.format(run_name, num, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), i, jinb)
                    sava_txt(gStr)
                    if stop_num > 1:
                        stop_state = True
                        sava_txt('今日回帖金币已满，程序将自动终止...')
                        break
                else:
                    if '抱歉，验证码填写错误' in value:
                        state = '本次回帖需要验证码'
                    elif '抱歉，您两次发表间隔少于' in value:
                        state = '本次回帖回复太快了，等待10秒'
                        time.sleep(10)
                    elif '回复需要审核' in value:
                        state = '本次回帖需要审核，应该是该贴已经回复过了或回复内容太相似了'
                    elif '抱歉，本帖要求阅读权限高于' in value:
                        state = '本次回帖失败，你所在的用户组权限不够不能回复此贴'
                    elif '抱歉，您所在的用户组每小时限制' in value:
                        state = '本次回帖受到小时限制了'
                        sleep_state = True
                    elif value == -1:
                        state = '访问异常，请稍后再试'
                        cep_num += 1
                        if cep_num > 2:
                            stop_state = True
                            sava_txt('今日回帖访问异常，程序将自动终止...')
                            break
                    else:
                        state = '未知错误，详情查看日志'
                        cep_num += 1
                        if cep_num > 2:
                            stop_state = True
                            sava_txt('今日回帖未知错误，程序将自动终止...')
                            break
                    gStr = '{} {} {} 第{}页 金币{} 回帖失败，原因【{}】'.format(run_name, num, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), i, jinb, state)
                    sava_txt(gStr)
                num += 1
                if sleep_state:
                    second = 3605-(int(time.time())-start_time)
                    sava_txt('回帖受到限制，等待{}秒后继续...'.format(second))
                    time.sleep(second)
                    sleep_state = False
                    start_state = True
                else:
                    second = randint(self.bbs_dict['reply_second'], self.bbs_dict['reply_second']+3)
                    sava_txt('回帖有间隔，等待{}秒后继续...'.format(second))
                    time.sleep(second)
            if stop_state:
                break
        sava_txt('-----{}任务终止，结束{}为{}-----'.format(run_name, self.bbs_dict['jinb_name'], jinb))

    def suiji_uid(self):
        passwd = random.sample(string.ascii_letters + string.digits, 8)
        return ''.join(passwd)

    def get_jinbi(self):
        url = "{}/home.php?mod=spacecp&ac=credit&showcredit=1&inajax=1&ajaxtarget=extcreditmenu_menu".format(self.bbs_dict['host'])
        try:
            r = requests.post(url, headers=self.headers, verify=False)
            uls = re.findall("<li>(.*?)</li>", r.text)
            for ul in uls:
                if self.bbs_dict['jinb_name'] in ul:
                    jinb_num = re.findall("\">(.*?)</span>", ul)[0]
                    return jinb_num
        except:
            return '查询异常'

class my_thread(threading.Thread):
    def __init__(self, bbs_dict):
        threading.Thread.__init__(self)
        self.bbs_dict = bbs_dict
    def run(self):
        reply_main(self.bbs_dict)

def main(bbs_dict):
    th = my_thread(bbs_dict)  # id, name
    th.start()

def reply_main(bbs_dict):
    try:
        d = dzReply(bbs_dict)
        d.get_tid()
    except:
        sava_txt('-----【程序运行异常】-----】\n{}'.format(traceback.format_exc()))

def sign(bbs_dict):
    url = "{}/plugin.php?id=dc_signin:sign&inajax=1&formhash={}&signsubmit=yes&handlekey=signin&emotid=1&referer={}&content=%E8%AE%B0%E4%B8%8A%E4%B8%80%E7%AC%94%EF%BC%8Chold%E4%BD%8F%E6%88%91%E7%9A%84%E5%BF%AB%E4%B9%90%EF%BC%81".format(
        bbs_dict['host'], bbs_dict['formhash'], bbs_dict['host'])
    headers['cookie'] = bbs_dict['cookie']
    try:
        r = requests.post(url, headers=headers, verify=False)
        print(r.text)
        if '签到成功' in r.text:
            signin = '签到成功~'
        elif '今日已经签' in r.text:
            signin = '您今日已经签过到~~'
        else:
            signin = '签到异常~'
        # signin = re.findall("{.*?_signin\('(.*?)',", r.text)[0]
        sava_txt('【{}】{} {}'.format(bbs_dict['bbs_name'], bbs_dict['user_name'], signin))
    except:
        sava_txt('-----【程序运行异常】-----】\n{}'.format(traceback.format_exc()))

def sava_txt(str):
    # print(str)
    with open("C:\inetpub\wwwroot\dz_info.txt", "a", encoding='gbk') as f:
        f.write(str+"\n")