import requests
import re
from hashlib import sha1
def login():
    login_url = 'http://sso-dev.591iq.cn/login?flag=login'
    user_url = 'http://gateway-dev.591iq.cn/base/workbench/build?appId=150636'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    psw = sha1()
    psw.update("123456".encode('utf8'))
    userPwd = psw.hexdigest()
    dict = {
        'userName': 'admin',
        # 'userPwd': '7c4a8d09ca3762af61e59520943dc26494f8941b',
        'userPwd': userPwd
    }
    loginR = requests.post(login_url,headers=headers,data=dict)
    AccessToken = loginR.cookies["IQ_SSO_Token"]
    get_id(AccessToken)
def get_id(AccessToken):
    url = 'http://base-dev.591iq.cn/student/student!pageStudent.do'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'Cookie' : 'IQ_SSO_Token=%s; ' % AccessToken
    }
    data = {
        'rows': 5000,
        'classId': 'B8BB445D80DE11E8952C00163E0411B9'
    }
    r = requests.post(url,headers=headers,data=data).text
    zz = re.compile('"educationNumber":"(.*?)"',re.S)
    ids = re.findall(zz,r)
    print(len(ids))
    # for id in ids:
    #     print(id)
    for i in range(len(ids)):
        print(ids[i])
        # with open('txt\\qzex_stuId.txt', 'a', encoding='utf-8') as file:
        #     file.write(id+'\n')
login()