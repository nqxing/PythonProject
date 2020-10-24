import requests
from hashlib import sha1
import json
import re
# 登录方法，多学校正式服
def login():
    AJlist = []
    f = open(r"D:\PythonProject\IQ\base2\txt\data.txt", "r")
    lines = f.readlines()  # 读取全部内容
    userList = lines[0].strip().split(',')
    userName = userList[0]
    pwd = userList[1]
    login_url = 'http://sso.591iq.cn/login?flag=login'
    user_url = 'http://gateway.591iq.cn/base/workbench/build?appId=150636'
    headers0 = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    psw = sha1()
    psw.update(pwd.encode('utf8'))
    userPwd = psw.hexdigest()
    dict = {
        'userName': userName,
        'userPwd': userPwd
    }
    loginR = requests.post(login_url,headers=headers0,data=dict)
    AccessToken = loginR.cookies["IQ_SSO_Token"]
    AJlist.append(AccessToken)
    headers0['AccessToken'] = AccessToken
    headers0['AppKey'] = '02619EF1A99F54F199590E871ED8B9C2'
    userR = requests.get(user_url,headers=headers0)
    zz = re.compile('"managerCenterUrl":"(.*?)"',re.S)
    sidUrl = re.findall(zz,userR.text)
    headers1={}
    headers1['Cookie'] = 'IQ_SSO_Token='+AccessToken+';'
    sidR = requests.get(sidUrl[0],headers=headers1)
    JSESSIONID = sidR.cookies["JSESSIONID"]
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'Cookie' : 'IQ_SSO_Token=%s; JSESSIONID=%s'%(AccessToken,JSESSIONID)
    }
    return headers
# 获取学校名字
def get_SchName():
    headers = login()
    url = 'http://base.591iq.cn/organization/organization!pageSchoolList.do'
    r = requests.post(url,headers=headers).text
    Jdata = json.loads(r)
    school = Jdata['schoolList']
    zz = re.compile('"name":"(.*?)"',re.S)
    name = re.findall(zz,school)
    return name[0]
# 获取学生信息
def get_Student():
    headers = login()
    url = 'http://base.591iq.cn/student/student!pageStudent.do'
    data = {
        'rows': 5000,
        'classId': '-1'
    }
    r = requests.post(url,headers=headers,data=data).text
    Jdata = json.loads(r)
    return Jdata
# 获取老师信息
def get_Teacher():
    headers = login()
    url = 'http://base.591iq.cn/teacher/teacher!pageTeacher.do'
    data = {
        'rows': 5000,
        'classId': '-1'
    }
    r = requests.post(url,headers=headers,data=data).text
    Jdata = json.loads(r)
    return Jdata
# 获取年级信息
def get_Grade():
    headers = login()
    url = 'http://base.591iq.cn/grade/grade!pageGradeList.do'
    data = {
        'page': 1,
        'rows': 20
    }
    r = requests.post(url,headers=headers,data=data).text
    Jdata = json.loads(r)
    return Jdata
# 获取班级信息
def get_Class():
    headers = login()
    url = 'http://base.591iq.cn/administrative/administrative!getAdminClass.do'
    r = requests.post(url,headers=headers).text
    Jdata = json.loads(r)
    return Jdata
# 获取学年，学期信息
def get_Semester():
    headers = login()
    url = 'http://base.591iq.cn/semester/semester!get.do?sfunname='
    data = {
        'page': 1,
        'rows': 20
    }
    r = requests.post(url,headers=headers,data=data).text
    Jdata = json.loads(r)
    return Jdata
# 获取作息时间信息
def get_Section():
    headers = login()
    url = 'http://base.591iq.cn/section/section!list.do'
    r = requests.post(url,headers=headers).text
    Jdata = json.loads(r)
    return Jdata
# 获取建筑信息
def get_Building():
    headers = login()
    url = 'http://base.591iq.cn/building/building!get.do'
    data = {
        'page': 1,
        'rows': 20
    }
    r = requests.post(url,headers=headers,data=data).text
    Jdata = json.loads(r)
    return Jdata
# 获取教室信息
def get_Classroom():
    headers = login()
    url = 'http://base.591iq.cn/classroom/classroom!get.do'
    data = {
        'page': 1,
        'rows': 500
    }
    r = requests.post(url,headers=headers,data=data).text
    Jdata = json.loads(r)
    return Jdata
get_SchName()