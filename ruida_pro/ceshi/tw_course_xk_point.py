import requests
import json
from urllib import parse

class course:
    '天蛙微信选课测试-选课点'
    def __init__(self):
        self.url = 'http://dev-service.591iq.com.cn/thirdAccount/login'
        self.xk_url = 'http://gateway-test.591iq.com.cn/apps/course/select/point/pointTaskCourse/inputPoint'
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
            "AppKey":"02619EF1A99F54F199590E871ED8B9C2",
            "Content-Type": "application/json"
        }
        dict = json.dumps(
            [{"classId": "C8A1D8710B87D7324115EAD863AADF97", "point": 50,
              "pointTaskCourseId": "5460C7163A5A99859E2877B28974C886",
              "pointTaskId": "6966BBB19DC994702F990BF36B57EC61"},
             {"classId": "B9985C5CE68984341B1009D247695CBA", "point": 60,
              "pointTaskCourseId": "5460C7163A5A99859E2877B28974C886",
              "pointTaskId": "6966BBB19DC994702F990BF36B57EC61"},
             {"classId": "7F0F50B9D1F249B8F44A48A862F9FB87", "point": 80,
              "pointTaskCourseId": "A875DF93C247A024A64DC61E4C00C0F9",
              "pointTaskId": "6966BBB19DC994702F990BF36B57EC61"},
             {"classId": "463C771524A8B523A9EC91B560A0DDFF", "point": 100,
              "pointTaskCourseId": "A875DF93C247A024A64DC61E4C00C0F9",
              "pointTaskId": "6966BBB19DC994702F990BF36B57EC61"}]
        )
        r = requests.post(self.xk_url, headers=headers,data=dict)
        print(r.text)
    def main(self):
        f = open("txt\\id_2.txt", "r")
        lines = f.readlines()  # 读取全部内容
        for line in lines:
            self.login_tw(line.strip())
if __name__ == '__main__':
    c = course()
    c.main()