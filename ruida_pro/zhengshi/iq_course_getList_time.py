import requests
import re
# 学生登录，获取时间优先选课列表课程
id = 1
def login(name):
    url = 'http://sso.591iq.cn/login?flag=login'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    dict = {
        'userName': name,
        'userPwd': 'e36574187c4f3a75ecbda9ff04bbd61fac617163'
    }
    res = requests.post(url,headers=headers,data=dict)
    AccessToken = res.cookies["IQ_SSO_Token"]
    getlist(AccessToken)
def getlist(AccessToken):
    url = 'http://gateway.591iq.cn/apps/course/select/time/timeSelectCourse/optionalCourseList'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'AppKey': '02619EF1A99F54F199590E871ED8B9C2',
        'AccessToken': AccessToken
    }
    r = requests.post(url,headers=headers).text
    zz = re.compile('"courseInfoName":"(.*?)"',re.S)
    st = re.findall(zz,r)
    st = list(set(st))
    global id
    print('%d: %s门课程,%s' % (id,len(st),st))
    id+=1
def main():
    f = open("txt\\xmlz_stuId.txt", "r")
    lines = f.readlines()  # 读取全部内容
    for line in lines:
        login(line.strip())
main()