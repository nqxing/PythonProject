import requests
import json
from urllib import parse
import hashlib
from urllib.parse import quote

class getStudent:
    '天蛙PC端获取学生账号-测试环境'
    def __init__(self):
        self.login_url = 'http://dev-service.591iq.com.cn/account/login'
        self.cx_url = 'http://dev-service.591iq.com.cn/studentMgr/searchBack'
    def login_tw(self,userList):
        id = userList[0]
        pwd = userList[1]
        userPwd = hashlib.md5()
        userPwd.update(pwd.encode('utf8'))
        userPwd = userPwd.hexdigest()
        dict = {
        "request": {"encryptType":0,"data":{"loginName":id,"password":userPwd},"session":"null","datetime":1539156242144}
        }
        self.headers = {
            "clientos":"105",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        }
        data= bytes(parse.urlencode(dict), encoding='utf-8')
        r = requests.post(self.login_url,params=data,headers=self.headers)
        j = json.loads(r.text)
        session = j['session']
        self.searchBack(session)
    def searchBack(self,session):
        dict = '{"encryptType":0,"data":{"offset":"0","limit":"10","studentName":"","doType":"1","classId":"","gradeId":""},"session":"%s","datetime":1539222197824}'%session
        text = 'request=' + quote(dict, 'utf-8')
        r = requests.post(self.cx_url,params=text,headers=self.headers).text
        print(r)
    def main(self):
        f = open("txt\\tw_dev_user.txt", "r")
        lines = f.readlines()  # 读取全部内容
        for line in lines:
            userList = line.strip().split(',')
            self.login_tw(userList)
if __name__ == '__main__':
    c = getStudent()
    c.main()