import requests
import os
class getBase():
    '''
    获取测试服基础学生学籍号 写入txt文件
    '''
    def __init__(self):
        self.log_url = 'http://gateway2-test.591iq.com.cn/apps/base/user/ssoLogin'
        self.stu_url = 'http://gateway2-test.591iq.com.cn/apps/base/school/student/list'
        self.headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
            'AppKey': '02619EF1A99F54F199590E871ED8B9C2'
        }
    def login(self):
        dirPath = "id.txt"
        if (os.path.exists(dirPath)):
            os.remove(dirPath)
        f = open("user_test.txt", "r")
        lines = f.readlines()  # 读取全部内容
        userList = lines[0].split(',')
        dict = {
            'userName': userList[0],
            'userPwd': userList[1]
        }
        r = requests.post(self.log_url,headers=self.headers,data=dict).json()
        self.headers['AccessToken'] = r['data']['accessToken']
        for c in range(250,259):
            self.getStu(c,7)
    # 输入班级id 和年级id
    def getStu(self,classId,gradeId):
        dict = {
            'rows': 2,
            'page': 1,
            'classId': classId,
            'gradeId': gradeId,
            'schoolId': 7,
            'sort': 'false'
        }
        r = requests.post(self.stu_url,headers=self.headers,data=dict).json()
        rows = r['data']['rows']
        for i in range(len(rows)):
            if 'educationNumber' in rows[i]:
                educationNumber = rows[i]['educationNumber']
            else:
                educationNumber = '空'
            if 'className' in rows[i]:
                className = rows[i]['className']
            else:
                className = '空'
            data = '{},{}'.format(educationNumber,className)
            with open("id.txt", "a", encoding='utf-8') as f:
                f.write(str(data)+'\n')
if __name__ == '__main__':
    o = getBase()
    o.login()