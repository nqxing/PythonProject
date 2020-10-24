import requests
import re
from hashlib import sha1
import json
import xlwt
import time
class getStudent:
    def __init__(self):
        self.login_url = 'http://sso.591iq.cn/login?flag=login'
        self.user_url = 'http://gateway.591iq.cn/base/workbench/build?appId=150636'
        self.cx_url = 'http://base.591iq.cn/student/student!pageStudent.do'
        self.classNameList = []
        self.userNameList = []
        self.userPwdList = []
        self.sheetList = []
        self.title = ['姓名', '拼音', '年级', '班级', '学号', '学籍号', '身份证', '录入时间']
        self.title_style = xlwt.easyxf('font: height 360;')  # 定义标题单元格高度
        self.content_style = xlwt.easyxf('font: height 300;')  # 定义非标题单元格高度
        self.styleTitle = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
        self.styleContent = xlwt.XFStyle()  # 创建一个样式对象，初始化样式

    def login(self,userName,userPwd):
        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        }
        psw = sha1()
        psw.update(userPwd.encode('utf8'))
        userPwd = psw.hexdigest()
        dict = {
            'userName': userName,
            'userPwd': userPwd
        }
        loginR = requests.post(self.login_url, headers=headers, data=dict)
        AccessToken = loginR.cookies["IQ_SSO_Token"]
        headers['AccessToken'] = AccessToken
        headers['AppKey'] = '02619EF1A99F54F199590E871ED8B9C2'
        userR = requests.get(self.user_url, headers=headers)
        zz = re.compile('"managerCenterUrl":"(.*?)"', re.S)
        sidUrl = re.findall(zz, userR.text)
        headers1 = {}
        headers1['Cookie'] = 'IQ_SSO_Token=' + AccessToken + ';'
        sidR = requests.get(sidUrl[0], headers=headers1)
        JSESSIONID = sidR.cookies["JSESSIONID"]
        headers2 = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
            'Cookie': 'JSESSIONID=%s; IQ_SSO_Token=%s' % (JSESSIONID, AccessToken)
        }
        data = {
            'rows': 5000,
            'classId': '-1'
        }
        r = requests.post(self.cx_url, headers=headers2, data=data).text
        return r
    def setList(self):
        f = open("txt\\iq_userdata.txt", "r")
        lines = f.readlines()  # 读取全部内容
        for line in lines:
            userList = line.strip().split(',')
            self.classNameList.append(userList[0])
            self.userNameList.append(userList[1])
            self.userPwdList.append(userList[2])
        self.book = xlwt.Workbook()  # 新建一个excel对象
        for c in range(len(self.classNameList)):
            sheetName = self.book.add_sheet(self.classNameList[c])  # 添加一个sheet页
            self.sheetList.append(sheetName)
    def main(self):
        self.setList()
        for i in range(len(self.sheetList)):
            # 设置每一列的宽度
            first_col1 = self.sheetList[i].col(0)  # xlwt中是行和列都是从0开始计算的
            first_col1.width = 178 * 25
            first_col2 = self.sheetList[i].col(1)  # xlwt中是行和列都是从0开始计算的
            first_col2.width = 256 * 25
            first_col3 = self.sheetList[i].col(2)  # xlwt中是行和列都是从0开始计算的
            first_col3.width = 178 * 25
            first_col4 = self.sheetList[i].col(3)  # xlwt中是行和列都是从0开始计算的
            first_col4.width = 178 * 25
            first_col5 = self.sheetList[i].col(4)  # xlwt中是行和列都是从0开始计算的
            first_col5.width = 256 * 25
            first_col6 = self.sheetList[i].col(5)  # xlwt中是行和列都是从0开始计算的
            first_col6.width = 320 * 25
            first_col7 = self.sheetList[i].col(6)  # xlwt中是行和列都是从0开始计算的
            first_col7.width = 320 * 25
            first_col8 = self.sheetList[i].col(7)  # xlwt中是行和列都是从0开始计算的
            first_col8.width = 320 * 25
            # 设置应用标题的高度
            first_row = self.sheetList[i].row(0)
            first_row.set_style(self.title_style)
            # 设置单元格样式
            al = xlwt.Alignment()
            al.horz = 0x02  # 设置水平居中
            al.vert = 0x01  # 设置垂直居中
            fnt = xlwt.Font()
            fnt.bold = True    # 字体加粗
            fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
            fnt.colour_index = 2  # 字体红色
            # 应用单元格样式
            self.styleTitle.alignment = al
            self.styleTitle.font = fnt
            self.styleContent.alignment = al
            for j in range(len(self.title)):
                # title多长，循环几次
                self.sheetList[i].write(0, j, self.title[j], self.styleTitle)
            r = self.login(self.userNameList[i],self.userPwdList[i])
            data = json.loads(r)
            rows = data['rows']
            lists = []
            for row in rows:
                dic = {}
                if 'name' in row:
                    name = row['name']
                else:
                    name = '空'
                if 'realNamePinyin' in row:
                    realNamePinyin = row['realNamePinyin']
                else:
                    realNamePinyin = '空'
                if 'gradeName' in row:
                    gradeName = row['gradeName']
                else:
                    gradeName = '空'
                if 'className' in row:
                    className = row['className']
                else:
                    className = '空'
                if 'studentNumber' in row:
                    studentNumber = row['studentNumber']
                else:
                    studentNumber = '空'
                if 'educationNumber' in row:
                    educationNumber = row['educationNumber']
                else:
                    educationNumber = '空'
                if 'idCardNumber' in row:
                    idCardNumber = row['idCardNumber']
                else:
                    idCardNumber = '空'
                if 'createTime' in row:
                    createTime = row['createTime']
                else:
                    createTime = '空'
                dic['name'] = name
                dic['realNamePinyin'] = realNamePinyin
                dic['gradeName'] = gradeName
                dic['className'] = className
                dic['studentNumber'] = studentNumber
                dic['educationNumber'] = educationNumber
                dic['idCardNumber'] = idCardNumber
                dic['createTime'] = createTime
                lists.append(dic)
            for num in range(len(lists)):
                first_row1 = self.sheetList[i].row(num + 1)
                first_row1.set_style(self.content_style)
                name1 = lists[num]['name']
                realNamePinyin1 = lists[num]['realNamePinyin']
                gradeName1 = lists[num]['gradeName']
                className1 = lists[num]['className']
                studentNumber1 = lists[num]['studentNumber']
                educationNumber1 = lists[num]['educationNumber']
                idCardNumber1 = lists[num]['idCardNumber']
                createTime1 = lists[num]['createTime']
                new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
                # 要从第二行开始写，所以这里行数要加1
                self.sheetList[i].write(new_row, 0, name1, self.styleContent)
                self.sheetList[i].write(new_row, 1, realNamePinyin1, self.styleContent)
                self.sheetList[i].write(new_row, 2, gradeName1, self.styleContent)
                self.sheetList[i].write(new_row, 3, className1, self.styleContent)
                self.sheetList[i].write(new_row, 4, studentNumber1, self.styleContent)
                self.sheetList[i].write(new_row, 5, educationNumber1, self.styleContent)
                self.sheetList[i].write(new_row, 6, idCardNumber1, self.styleContent)
                self.sheetList[i].write(new_row, 7, createTime1, self.styleContent)
                # print('已写入', num + 1, '条数据~~')
            self.book.save('txt\\智慧学生信息.xls')
            print(self.classNameList[i],'爬取成功~')
            time.sleep(2)
        # self.book.save('txt\\学生信息.xls')
if __name__ == '__main__':
    g = getStudent()
    g.main()