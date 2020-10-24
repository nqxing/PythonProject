import requests
import re
from hashlib import sha1
def login():
    login_url = 'http://sso-test.591iq.com.cn/login?flag=login'
    user_url = 'http://gateway-test.591iq.com.cn/base/workbench/build?appId=150636'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    psw = sha1()
    psw.update("123456".encode('utf8'))
    userPwd = psw.hexdigest()
    dict = {
        'userName': 'xmlz_admin',
        # 'userPwd': '7c4a8d09ca3762af61e59520943dc26494f8941b',
        'userPwd': userPwd
    }
    loginR = requests.post(login_url,headers=headers,data=dict)
    AccessToken = loginR.cookies["IQ_SSO_Token"]
    headers['AccessToken'] = AccessToken
    headers['AppKey'] = '02619EF1A99F54F199590E871ED8B9C2'
    userR = requests.get(user_url,headers=headers)
    zz = re.compile('"managerCenterUrl":"(.*?)"',re.S)
    sidUrl = re.findall(zz,userR.text)
    headers1={}
    headers1['Cookie'] = 'IQ_SSO_Token='+AccessToken+';'
    sidR = requests.get(sidUrl[0],headers=headers1)
    JSESSIONID = sidR.cookies["JSESSIONID"]
    get_id(JSESSIONID,AccessToken)
def get_id(JSESSIONID,AccessToken):
    url = 'http://base-test.591iq.com.cn/student/student!pageStudent.do'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'Cookie' : 'JSESSIONID=%s; IQ_SSO_Token=%s'%(JSESSIONID,AccessToken)
    }
    data = {
        'rows': 5000,
        'classId': '249209B3FD0D4EC895AE810D209EAC9D'
    }
    r = requests.post(url,headers=headers,data=data).text
    # print(r)
    zz = re.compile('"educationNumber":"(.*?)"',re.S)
    ids = re.findall(zz,r)
    print(len(ids))
# for id in ids:
#     with open('txt\\qzex_stuId.txt', 'a', encoding='utf-8') as file:
#         file.write(id+'\n')
login()