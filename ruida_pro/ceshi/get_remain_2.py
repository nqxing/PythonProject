import requests
import json

# 获取学生最新选课点点数减去本地txt选课点，测试补录学生选课点点数是否正确
remainPoints = []
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
    url = 'http://gateway-test.591iq.com.cn/apps/course/select/point/pointAccount/get'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'AppKey': '02619EF1A99F54F199590E871ED8B9C2',
        'AccessToken': AccessToken
    }
    r = requests.post(url,headers=headers).text
    j = json.loads(r)
    numid = j['data']
    remainPoints.append(numid['remainPoint'])
def main():
    f = open("txt\\studentNumber.txt", "r")
    lines = f.readlines()  # 读取全部内容
    for line in lines:
        login(line.strip())
    f1 = open("txt\\remainPoint.txt", "r")
    lines1 = f1.readlines()  # 读取全部内容
    for (line1,remainPoint) in zip(lines1,remainPoints):
        num = remainPoint-int(line1)
        print(num)
main()