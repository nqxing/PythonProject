import requests
import json
from urllib import parse
import re
import hashlib

class course:
    '天蛙微信选课测试-时间优先'
    def __init__(self):
        self.url = 'https://service.591iq.cn/thirdAccount/login'
        self.xk_url = 'https://gateway.591iq.cn/apps/course/select/time/timeSelectCourse/optionalCourseList'
        self.id = 1
    def login_tw(self,id):
        pwd = id[-6:]
        userPwd = hashlib.md5()
        userPwd.update(pwd.encode('utf8'))
        userPwd = userPwd.hexdigest()
        dict = {
        "request": {"encryptType":0,"data":{"account":id,"pwd":userPwd,"code":"","type":"wx","tparam":"","timestamp":1538274577755},"session":""}
        }
        headers = {
            "clientos":"105"
        }
        data= bytes(parse.urlencode(dict), encoding='utf-8')
        r = requests.post(self.url,params=data,headers=headers)
        j = json.loads(r.text)
        ssoToken = j['ssoToken']
        self.course_xk(ssoToken)
    def course_xk(self,ssoToken):
        headers = {
            "AccessToken":ssoToken,
            "AppKey":"02619EF1A99F54F199590E871ED8B9C2"
        }
        r = requests.post(self.xk_url, headers=headers).text
        zz = re.compile('"courseInfoName":"(.*?)"', re.S)
        st = re.findall(zz, r)
        st = list(set(st))
        print('%d: %s门课程,%s' % (self.id, len(st), st))
        self.id += 1
    def main(self):
        f = open("txt\\xmlz_stuId.txt", "r")
        lines = f.readlines()  # 读取全部内容
        for line in lines:
            self.login_tw(line.strip())
if __name__ == '__main__':
    c = course()
    c.main()