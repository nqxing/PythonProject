import requests
import re
import json
from hashlib import sha1
#  多学校测试服 获取选课任务可选的所有行政班，再根据行政班列出所有可选课程
def login():
    login_url = 'http://sso2-test.591iq.com.cn/login?flag=login'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    # psw = sha1()
    # psw.update("123456".encode('utf8'))
    # psw.update("fzssz123456".encode('utf8'))
    # userPwd = psw.hexdigest()
    dict = {
        # 'userName': 'fzssz_admin',
        'userName': 'xmlz_admin',
        'userPwd': '123456'
    }
    loginR = requests.post(login_url,headers=headers,data=dict)
    AccessToken = loginR.cookies["IQ_SSO_Token"]
    get_course(AccessToken)

def sort_key(s):
    # 排序关键字匹配
    # 匹配数字序号
    if s:
        try:
            c = re.findall(r'(\d+)', s)[0]
        except:
            c = -1
        return int(c)
def strsort(alist):
    alist.sort(key=sort_key)
    return alist

def get_course(AccessToken):
    url = 'http://gateway-test.591iq.com.cn/apps/course/select/time/timeApproveCourse/getTimeTaskCourseList'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'AccessToken' : AccessToken,
        'AppKey': '02619EF1A99F54F199590E871ED8B9C2'
    }
    data = {
        'rows': 100,
        'page': 1,
        'semesterId': 10190,
        'timeTaskId': '72C7F170713A7E6881539AAE0FE38AB4'
    }
    r = requests.post(url,headers=headers,data=data).text
    # print(r)
    zz = re.compile('"adminClassName":"(.*?)"',re.S)
    # 拿到所有班级
    allClassList = re.findall(zz,r)
    # 班级累加
    strClassList = ''
    for c in allClassList:
        strClassList+=c+','
    # 去除字符串最后一个字符
    strClassList = strClassList[:-1]
    # 切割成列表
    ClassList = strClassList.split(',')
    # 列表去重方法
    ClassList = list(set(ClassList))
    # 调用排序方法按数字大小排序班级
    ClassList = strsort(ClassList)
    print(len(ClassList),'个班级',ClassList)
    j = json.loads(r)
    TaskCourseList = j['rows']
    allClassCourse = []
    for class_ in ClassList:
        dic = dict()
        for t in TaskCourseList:
            courseInfoName = t['courseInfoName']
            adminClassRangeList = t['adminClassRangeList']
            ClassNameList = adminClassRangeList[0]['adminClassName'].split(',')
            if class_ in ClassNameList:
                dic.setdefault(class_, []).append(courseInfoName)
        allClassCourse.append(dic)
    for c in ClassList:
        for a in allClassCourse:
            if c in a:
                CourseList = a[c]
                print('{}：可选{}门课程,{}'.format(c,len(CourseList),CourseList))
login()