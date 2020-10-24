import requests
import json
import re
class getStuid:
    '''
    时间优先添加指定学生界面获取学生账号，并截取后6位密码
    '''
    def __init__(self):
        self.url = 'http://gateway-dev.591iq.cn/apps/course/select/setting/studentAndTransClass/getTimeNoStudent'
        self.dict = {
            'rows': 10,
            'page': 1,
            'id': 'B9005CC84531FF77FBFEADBC248093F2',
            'gradeId': '6DC08C24C63949369640E4C65744F9F9',
            'gradeCourseId': '0469F417DB09C46F9A8186E6E3A38379',
            'subjectId': '03E590C15A4D615602FE5329EF204876',
            'semesterId': '33EF67B43B6D4FC182034FA1C67FAE19'
        }
    def login(self):
        url = 'http://sso-test.591iq.com.cn/login?flag=login'
        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        }
        dict = {
            'serviceUrl': 'http://web-test.591iq.com.cn/apps/course/index.html',
            'userName': 'rd_admin',
            'userPwd': '7c4a8d09ca3762af61e59520943dc26494f8941b'
        }
        res = requests.post(url, headers=headers, data=dict)
        AccessToken = res.cookies["IQ_SSO_Token"]
        self.get_id(AccessToken)
    def get_id(self,AccessToken):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'AccessToken': AccessToken,
            'AppKey': '02619EF1A99F54F199590E871ED8B9C2'
        }
        r = requests.post(self.url,headers=headers,data=self.dict).text
        j = json.loads(r)
        numid = j['rows']
        zz = re.compile("'studentNumber': '(.*?)'",re.S)
        for n in numid:
            id = re.findall(zz,str(n))
            name = str(id[0])
            pwd = name[-6:]
            print(name+','+pwd)
if __name__ == '__main__':
    c = getStuid()
    c.login()