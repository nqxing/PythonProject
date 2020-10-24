import requests
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
        f = open("txt\\user_test.txt", "r")
        lines = f.readlines()  # 读取全部内容
        userList = lines[0].split(',')
        dict = {
            'userName': userList[0],
            'userPwd': userList[1]
        }
        r = requests.post(self.log_url,headers=self.headers,data=dict).json()
        self.headers['AccessToken'] = r['data']['accessToken']
        # print(r)
        # print(self.headers)
        # 学校id
        self.getStu(1)
    def getStu(self,sId):
        dict = {
            'rows': 10000,
            'page': 1,
            'gradeId': 3,
            'schoolId': sId
        }
        # dict1 = {
        #     'rows': 10000,
        #     'page': 1,
        #     'classId': 1230,
        #     'gradeId': 3,
        #     'schoolId': 1,
        # }
        r = requests.post(self.stu_url,headers=self.headers,data=dict).json()
        rows = r['data']['rows']
        for r in rows:
            # className = r['className']
            className = "all"
            if 'educationNumber' in r:
                educationNumber = r['educationNumber']
            else:
                educationNumber = '空'
            with open("{}.txt".format(className), "a", encoding='utf-8') as f:
                f.write(str(educationNumber)+'\n')
if __name__ == '__main__':
    o = getBase()
    o.login()