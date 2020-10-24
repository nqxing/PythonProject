import requests
import re
class course:
    '''
    学生登录，依次勾选同一门课程选课
    '''
    def __init__(self):
        self.num = 1
    def login(self,name):
        url = 'http://sso.591iq.cn/login?flag=login'
        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        }
        dict = {
            'serviceUrl': 'http://web.591iq.cn/apps/course/index.html',
            'userName': name,
            'userPwd': '7c4a8d09ca3762af61e59520943dc26494f8941b'
        }
        res = requests.post(url,headers=headers,data=dict)
        AccessToken = res.cookies["IQ_SSO_Token"]
        self.getlist(AccessToken)
    def getlist(self,AccessToken):
        url = 'http://gateway.591iq.cn/apps/course/select/time/timeSelectCourse/optionalCourseList'
        xk_url = 'http://gateway.591iq.cn/apps/course/select/time/timeSelectCourse/courseJoinQueue'
        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
            'AppKey': '02619EF1A99F54F199590E871ED8B9C2',
            'AccessToken': AccessToken
        }
        dict = {
            'messages': '20A10231AAA4931452C04A05710F7135-E8BD0050CCD4502B6D36023FCE5214E1',
            'type': 1
        }
        r = requests.post(url,headers=headers).text
        zz = re.compile('"className":"(.*?)"',re.S)
        st = re.findall(zz,r)
        print(self.num,' : ',st)
        self.num+=1
        x = requests.post(xk_url,headers=headers,data=dict)
        print(x.text)
    def main(self):
        f = open("txt\\id.txt", "r")
        lines = f.readlines()  # 读取全部内容
        for line in lines:
            self.login(line.strip())
if __name__ == '__main__':
    c = course()
    c.main()