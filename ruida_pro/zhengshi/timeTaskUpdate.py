import requests
import json
from hashlib import sha1
#  多学校正式服 修改选课任务里面的选课时间

# beginDatetime = '2018-11-16 14:00:00'
# endDatetime = '2018-11-16 15:10:00'
# timeTaskId = '7D0116CD62E8CB06B284DAB043E45407'
beginDatetime = '2018-12-02 07:00:00'
endDatetime = '2018-12-02 20:00:00'
timeTaskId = 'D6242562A10A1E6E432A98CA338A348B'

def login():
    login_url = 'http://sso.591iq.cn/login?flag=login'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    psw = sha1()
    psw.update("ypzx123321".encode('utf8'))
    userPwd = psw.hexdigest()
    dict = {
        'userName': 'ypzx_admin',
        'userPwd': userPwd
    }
    loginR = requests.post(login_url,headers=headers,data=dict)
    AccessToken = loginR.cookies["IQ_SSO_Token"]
    get_course(AccessToken)
def get_course(AccessToken):
    url = 'http://gateway.591iq.cn/apps/course/select/time/timeApproveCourse/getTimeTaskCourseList'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'AccessToken' : AccessToken,
        'AppKey': '02619EF1A99F54F199590E871ED8B9C2'
    }
    data = {
        'rows': 100,
        'page': 1,
        'semesterId': '83E484D0CFFE420E91620E8920F6157F',
        'timeTaskId': timeTaskId
    }
    r = requests.post(url,headers=headers,data=data).text
    data = json.loads(r)
    rows = data['rows']
    for r in rows:
        update(r,headers)
def update(r,headers):
    url = 'http://gateway.591iq.cn/apps/course/select/time/timeApproveCourse/update'
    gradeCourseId = r['gradeCourseId']
    gradeId = r['gradeId']
    gradeName = r['gradeName']
    id = r['id']
    adminClassRangeList = r['adminClassRangeList']
    adminClassId = adminClassRangeList[0]
    ClassId = adminClassId['adminClassId']
    className = adminClassId['adminClassName']
    data = {
        'sbeginDatetime': beginDatetime,
        'sendDatetime': endDatetime,
        'gradeCourseIds': gradeCourseId,
        'selectType': 1,
        'isStrideGrade': 0,
        'gradeId': gradeId,
        'gradeName': gradeName,
        'classId': ClassId,
        'className': className,
        'id': id,
        'approveState': 2,
        'timeTaskId':'',
        'resetCourseState': 0
    }
    r = requests.post(url,headers=headers,data=data).text
    print(r)
login()