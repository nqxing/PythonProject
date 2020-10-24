import requests
import json
import time
import datetime

headers = {
    'AccessToken': '45204A0BDB1C0C47B03AF939A33785DF',
    'AppKey': '02619EF1A99F54F199590E871ED8B9C2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}
minutes1 = -1
minutes2 = 1

def xtime(t, s):
    timestring = "2019-09-05 {}:56".format(t)
    timestamp = time.mktime(time.strptime(timestring, '%Y-%m-%d %H:%M:%S'))
    datetime_struct = datetime.datetime.fromtimestamp(timestamp)
    datetime_obj = (datetime_struct + datetime.timedelta(minutes=s)).strftime('%H:%M')
    return datetime_obj
def get_stu_time():
    url = 'http://gateway-test.591iq.com.cn/common/baseInfo/getClassSectionList'
    r = requests.post(url, headers=headers)
    # print(r.text)
    datas = r.json()['data']
    for d in datas:
        startTimeStr = xtime(d['startTimeStr'], minutes1)
        endTimeStr = xtime(d['endTimeStr'], minutes2)
        daka_time = '{},{}'.format(startTimeStr, endTimeStr)
        with open("stu_time.txt", "a", encoding='utf-8') as f:
            f.write(str(daka_time) + '\n')
def stu_daka(users, str_date):
    users = users.split(',')
    headers['Content-Type'] = 'application/json'
    url = 'http://gateway-test.591iq.com.cn/apps/sign/sign/doSign'
    dic = {
        'classRoomId': "",
        'signTime': str_date,
        'terminalCommunicationNumber': "",
        'userId': "{}".format(users[0]),
        'userName': "test",
        'userType': 2
    }
    r = requests.post(url, headers=headers, data=json.dumps(dic))
    print(str_date, users[1], users[0], r.text)
date = '2019-09-05'
for id in open("id.txt", encoding='utf-8'):
    for s in open("stu_time.txt", encoding='utf-8'):
        times = s.strip().split(',')
        for t in times:
            str_date = '{} {}'.format(date, t)
            stu_daka(id.strip(), str_date)
    print('---------------------------------')

# get_stu_time()

def daka1(users, str_date):
    users = users.split(',')
    # headers = {
    #     'AccessToken': '45204A0BDB1C0C47B03AF939A33785DF',
    #     'AppKey': '02619EF1A99F54F199590E871ED8B9C2',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    #     'Content-Type': 'application/json'
    # }
    headers['Content-Type'] = 'application/json'
    url = 'http://gateway-test.591iq.com.cn/apps/sign/sign/doSign'
    dic = {
        'classRoomId': "",
        'signTime': str_date,
        'terminalCommunicationNumber': "",
        'userId': "{}".format(users[0]),
        'userName': "test",
        'userType': 2
    }
    r = requests.post(url, headers=headers, data=json.dumps(dic))
    print(str_date, users[1], users[0], r.text)

# daka1('138371,陈鑫', '2019-09-05 07:39')