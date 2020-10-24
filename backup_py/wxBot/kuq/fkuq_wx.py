import os
import re
import requests
import sqlite3
import time
# from wxpy import *
# from kuq.config.config1 import KUQ_PATH, KQ_TIME

KUQ_PATH = r'C:\CQA-xiaoi\data\2075160473\eventv2.db'
KUQ_IMAGE_PATH = r'C:\CQA-xiaoi\data\image\{}.cqimg'
KQ_TIME = 15  # 每隔多少秒查询一次聊天记录
GROUP_QQ = [931936320,608455861]
GROUP_WX = ['福利社']

def sava_img(img_url, img_name):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    try:
        img = requests.get(img_url, headers = headers)
        if img.status_code == 200:
            img_path = r'image\{}'.format(img_name)
            with open(img_path, "wb") as f:
                f.write(img.content)
            return True
        else:
            return False
    except:
        return False

def get_kq_text(text):
    img_files = re.findall("\[CQ:image,file=(.*?)\]", text)
    img_num = len(img_files)
    if img_num != 0:
        imgs_state = []
        for img in img_files:
            if(os.path.exists(KUQ_IMAGE_PATH.format(img))):
                f = open(KUQ_IMAGE_PATH.format(img), "r")
                lines = f.readlines()  # 读取全部内容
                img_url = lines[-2].strip().split('url=')
                sava_img_res = sava_img(img_url[-1], img)
                imgs_state.append({'state': sava_img_res, 'img_file': img})
            text = text.replace('[CQ:image,file={}]'.format(img), '')
        return text, imgs_state

def cx_content(kq_cursor, ticks):
    # 查询酷Q聊天记录库
    # kq_cursor.execute('''select content from event where time > %s and type is not Null''' % (ticks - cx_min * 60))
    kq_cursor.execute('''select `group`,content from event where time > %s ''' % (ticks))
    values = kq_cursor.fetchall()
    return values, len(values)

def kuq_main(bot):
    # 初始化机器人，扫码登陆
    # bot = Bot(cache_path=True)
    # bot.enable_puid('wxpy_puid.pkl')

    conn = sqlite3.connect(KUQ_PATH)  # 饿了么数据库地址
    cursor = conn.cursor()  # 获取游标
    # bianhao = 1  # 红包编号（也代表开了多少个异步线程）
    ticks = int(time.time()) #获取运行该脚本时的时间戳
    # ticks = 1573457087  # 获取运行该脚本时的时间戳
    stop_for = False
    x = 0
    print('QQ消息转发系统运行中...')
    while True:
        tup = cx_content(cursor, ticks)
        num = tup[1]  # 共获取到多少条聊天记录
        contents = tup[0]  # 聊天记录 数组里包元组格式
        # print(contents)
        # 该判断为每次未获取到新消息时就不进行聊天记录循环
        if num > x:
            new_contents = []
            i = num - x
            # 只对新消息进行循环，旧记录忽略
            for c in range(1, i + 1):
                content_state = False
                content = contents[-c][1]
                # print('消息 --》', content)
                for i in GROUP_QQ:
                    if str(i) in contents[-c][0]:
                        content_state = True
                if content_state:
                    # 判断是否为饿了么红包
                    if '[CQ:image,file=' in content:
                        res = get_kq_text(content)
                        new_contents.append({'text': res[0], 'imgs': res[1]})
                    else:
                        if len(content) != 0:
                            new_contents.append({'text': content, 'imgs': []})
                if '-!停止转发!-' == content:
                    stop_for = True
                    # logger.info('通过指令关闭了程序~')
                    break
            if len(new_contents) != 0:
                for n in new_contents:
                    send_msg(bot, n)
                    time.sleep(1)
            x = num
        if stop_for:
            break
        time.sleep(KQ_TIME)
    print('转发功能已关闭')

def send_msg(bot, wxmsg):
    for g in GROUP_WX:
        wxpy_groups = bot.search(g)
        if len(wxpy_groups) == 1:
            group = wxpy_groups[0]
            if len(wxmsg['text']) != 0:
                group.send('{}'.format(wxmsg['text']))
            if len(wxmsg['imgs']) != 0:
                for i in range(len(wxmsg['imgs'])):
                    if wxmsg['imgs'][i]['state']:
                        group.send_image('image/{}'.format(wxmsg['imgs'][i]['img_file']))
        else:
            fid = bot.search('/大号')[0]
            fid.send('消息转发失败，未找到或找到多个群聊名字[{}]'.format(g))
            fid.send(wxpy_groups)
# kuq_main(bot)

