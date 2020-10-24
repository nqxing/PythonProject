import requests
import re
# 学生登录，获取选课点选课列表课程
def login(name):
    url = 'http://sso-test.591iq.com.cn/login?flag=login'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    dict = {
        'serviceUrl': 'http://web-test.591iq.com.cn/apps/course/index.html',
        'userName': name,
        'userPwd': '7c4a8d09ca3762af61e59520943dc26494f8941b'
    }
    res = requests.post(url,headers=headers,data=dict)
    AccessToken = res.cookies["IQ_SSO_Token"]
    getlist(AccessToken)
def getlist(AccessToken):
    url = 'http://gateway-test.591iq.com.cn/apps/course/select/point/pointTaskCourse/list4student'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'AppKey': '02619EF1A99F54F199590E871ED8B9C2',
        'AccessToken': AccessToken
    }
    dict = {
        'rows': 10,
        'page': 1
    }
    r = requests.post(url,headers=headers,data=dict).text
    zz = re.compile('"className":"(.*?)"',re.S)
    st = re.findall(zz,r)
    print(st)
def main():
    f = open("txt\\id.txt", "r")
    lines = f.readlines()  # 读取全部内容
    for line in lines:
        login(line.strip())
main()