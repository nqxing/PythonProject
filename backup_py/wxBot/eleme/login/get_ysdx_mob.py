import requests
from pyquery import PyQuery as pq
# 禁用安全请求警告 关闭SSL验证时用
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pymysql,time,datetime
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49'
                  ' Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080'
}
HOST = '122.51.67.37'
USER = 'root'
# PWD = 'MUGVHmugvtwja116ye38b1jhb'
PWD = 'mm123456'
mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='public')
mysql_cursor = mysql_conn.cursor()  # 获取游标
def get_mob():
    num = 1
    for i in range(0, 10):
        mob_url = 'https://www.yinsiduanxin.com/china-phone-number/page/{}.html'.format(i+1)
        html = requests.get(mob_url, headers=HEADERS, timeout=25, verify=False)
        if html.status_code == 200:
            html = pq(html.text)
            layuis = html('.main .layui-row .card .layui-card').items()
            for layui in layuis:
                card_state = layui('.layui-card-header').text()
                if card_state == '在线':
                    mobile_url = layui('.layui-card-body p:nth-child(1) a').attr('href')
                    if 'china' in mobile_url:
                        mobile = layui('.layui-card-body p:nth-child(1)').attr('id')
                        mysql_cursor.execute("select * from pub_sms_list WHERE mobile = '{}'".format(mobile))
                        values = mysql_cursor.fetchall()
                        if values:
                            print('{} - 改号码已存库'.format(mobile))
                        else:
                            print(mobile, mobile_url)
                            mysql_cursor.execute(
                                "INSERT INTO pub_sms_list (mobile, mobile_url, note, create_time) VALUES ({}, 'https://www.yinsiduanxin.com{}', '未验证','{}')".format(mobile, mobile_url,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                            mysql_conn.commit()
                            print('{} - 已新增{}条记录~'.format(i+1, num))
                            num += 1
                    else:
                        print('非china号码')
        time.sleep(3)

get_mob()