import requests
import re
import time
class course:
    '''
    学生登录，依次勾选同一门课程选课
    '''
    def __init__(self):
        self.num = 1
    def login(self,name):
        url = 'http://sso-dev.591iq.cn/login?flag=login'
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
        xk_url = 'http://gateway-dev.591iq.cn/apps/course/select/time/timeSelectCourse/courseJoinQueue'
        ms_url = 'http://gateway-dev.591iq.cn/apps/course/common/mq/queryMessageQueueHandlerRslt'
        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
            'AppKey': '02619EF1A99F54F199590E871ED8B9C2',
            'AccessToken': AccessToken
        }
        xk_dict = {
            'messages': '51612A350F9572B2FD39EA0513635366-8960151F6DB7F571E3FD3E9B776D1BB5,19841E3DD29C4762CC69635B02CE9430-79BD105EE30D3786A34C086F02D6D590',
            'type': 1
        }
        ms_dict = {

        }
        r = requests.post(xk_url,headers=headers,data=xk_dict).text
        # print(r.text)
        zz = re.compile('"messageId":"(.*?)"',re.S)
        messageId = re.findall(zz,r)
        ms_dict['messageId'] =  messageId[0]
        time.sleep(2)
        m = requests.post(ms_url,headers=headers,data=ms_dict)
        print(self.num,r,m.text)
        self.num+=1
    def main(self):
        f = open("txt\\id.txt", "r")
        lines = f.readlines()  # 读取全部内容
        for line in lines:
            self.login(line.strip())
if __name__ == '__main__':
    c = course()
    c.main()