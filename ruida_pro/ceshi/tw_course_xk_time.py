import requests
import json
from urllib import parse

class course:
    '天蛙微信选课测试-时间优先'
    def __init__(self):
        self.url = 'http://dev-service.591iq.com.cn/thirdAccount/login'
        self.xk_url = 'http://gateway-test.591iq.com.cn/apps/course/select/time/timeSelectCourse/courseJoinQueue'
    def login_tw(self,id):
        dict = {
        "request": {"encryptType":0,"data":{"account":id,"pwd":"e10adc3949ba59abbe56e057f20f883e","code":"","type":"wx","tparam":"","timestamp":1535445650737},"session":""}
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
        dict = {
            "messages":"FA19DBE2BB4D8899D74F065FD6F2C2BF-B1354762D2E08F1B46A72C07BDB72E91,7BC97CA611E97C704111D7ABA5E68B73-02B04A43D2CE6C6D5E72875392661AA7",
            "type":1
        }
        r = requests.post(self.xk_url, headers=headers,data=dict)
        print(r.text)
    def main(self):
        f = open("txt\\id_1.txt", "r")
        lines = f.readlines()  # 读取全部内容
        for line in lines:
            self.login_tw(line.strip())
if __name__ == '__main__':
    c = course()
    c.main()