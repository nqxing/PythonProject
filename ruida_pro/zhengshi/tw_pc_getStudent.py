import requests
import json
from urllib import parse
import hashlib
from urllib.parse import quote
import xlwt
import time
class getStudent:
    '天蛙PC端获取学生账号-正式环境'
    def __init__(self):
        self.login_url = 'https://service.591iq.cn/account/login'
        self.cx_url = 'https://service.591iq.cn/studentMgr/searchBack'
        self.classNameList = []
        self.userNameList = []
        self.userPwdList = []
        self.sheetList = []
        self.title = ['姓名', '性别', '年级', '班级', '用户账号', '学籍号', '学籍辅号', '座号', '手机号码']
        self.title_style = xlwt.easyxf('font: height 360;')  # 定义标题单元格高度
        self.content_style = xlwt.easyxf('font: height 300;')  # 定义非标题单元格高度
        self.styleTitle = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
        self.styleContent = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
    def login_tw(self,id,pwd):
        userPwd = hashlib.md5()
        userPwd.update(pwd.encode('utf8'))
        userPwd = userPwd.hexdigest()
        dict = {
        "request": {"encryptType":0,"data":{"loginName":id,"password":userPwd},"session":"null","datetime":1539156242144}
        }
        self.headers = {
            "clientos":"105",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        }
        data= bytes(parse.urlencode(dict), encoding='utf-8')
        r = requests.post(self.login_url,params=data,headers=self.headers)
        j = json.loads(r.text)
        self.session = j['session']
        dict = '{"encryptType":0,"data":{"offset":"0","limit":"5000","studentName":"","doType":"1","classId":"","gradeId":""},"session":"%s","datetime":1539222197824}'%self.session
        text = 'request=' + quote(dict, 'utf-8')
        r = requests.post(self.cx_url,params=text,headers=self.headers).text
        return r
    def setList(self):
        f = open("txt\\tw_userdata.txt", "r")
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
            first_col2.width = 178 * 25
            first_col3 = self.sheetList[i].col(2)  # xlwt中是行和列都是从0开始计算的
            first_col3.width = 178 * 25
            first_col4 = self.sheetList[i].col(3)  # xlwt中是行和列都是从0开始计算的
            first_col4.width = 178 * 25
            first_col5 = self.sheetList[i].col(4)  # xlwt中是行和列都是从0开始计算的
            first_col5.width = 320 * 25
            first_col6 = self.sheetList[i].col(5)  # xlwt中是行和列都是从0开始计算的
            first_col6.width = 320 * 25
            first_col7 = self.sheetList[i].col(6)  # xlwt中是行和列都是从0开始计算的
            first_col7.width = 320 * 25
            first_col8 = self.sheetList[i].col(7)  # xlwt中是行和列都是从0开始计算的
            first_col8.width = 110 * 25
            first_col9 = self.sheetList[i].col(8)  # xlwt中是行和列都是从0开始计算的
            first_col9.width = 320 * 25
            # 设置应用标题的高度
            first_row = self.sheetList[i].row(0)
            first_row.set_style(self.title_style)
            # 设置单元格样式
            al = xlwt.Alignment()
            al.horz = 0x02  # 设置水平居中
            al.vert = 0x01  # 设置垂直居中
            fnt = xlwt.Font()
            fnt.bold = True  # 字体加粗
            fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
            fnt.colour_index = 2  # 字体红色
            # 应用单元格样式
            self.styleTitle.alignment = al
            self.styleTitle.font = fnt
            self.styleContent.alignment = al
            for j in range(len(self.title)):
                # title多长，循环几次
                self.sheetList[i].write(0, j, self.title[j], self.styleTitle)
            r = self.login_tw(self.userNameList[i], self.userPwdList[i])
            data = json.loads(r)
            data = data['data']
            rows = data['list']
            lists = []
            #        self.title = ['姓名', '性别', '年级', '班级', '用户账号', '学籍号', '学籍辅号', '座号']studentId
            for row in rows:
                dic = {}
                if 'studentName' in row:
                    studentName = row['studentName']
                else:
                    studentName = '空'
                if 'sex' in row:
                    if row['sex'] == '01':
                        sex = '男'
                    elif row['sex'] == '02':
                        sex = '女'
                    else:
                        sex = '未填写'
                else:
                    sex = '空'
                if 'gradeName' in row:
                    gradeName = row['gradeName']
                else:
                    gradeName = '空'
                if 'className' in row:
                    className = row['className']
                else:
                    className = '空'
                if 'individuationUname' in row:
                    individuationUname = row['individuationUname']
                else:
                    individuationUname = '空'
                if 'idNumber' in row:
                    idNumber = row['idNumber']
                else:
                    idNumber = '空'
                if 'studentCode' in row:
                    studentCode = row['studentCode']
                else:
                    studentCode = '空'
                if 'seatNum' in row:
                    seatNum = row['seatNum']
                else:
                    seatNum = '空'
                if 'studentId' in row:
                    studentId = row['studentId']
                else:
                    studentId = '空'
                dic['studentName'] = studentName
                dic['sex'] = sex
                dic['gradeName'] = gradeName
                dic['className'] = className
                dic['individuationUname'] = individuationUname
                dic['idNumber'] = idNumber
                dic['studentCode'] = studentCode
                dic['seatNum'] = seatNum
                dic['studentId'] = studentId
                lists.append(dic)
            for num in range(len(lists)):
                first_row1 = self.sheetList[i].row(num + 1)
                first_row1.set_style(self.content_style)
                studentName1 = lists[num]['studentName']
                sex1 = lists[num]['sex']
                gradeName1 = lists[num]['gradeName']
                className1 = lists[num]['className']
                individuationUname1 = lists[num]['individuationUname']
                idNumber1 = lists[num]['idNumber']
                studentCode1 = lists[num]['studentCode']
                seatNum1 = lists[num]['seatNum']
                studentId1 = lists[num]['studentId']
                url = 'https://service.591iq.cn/studentMgr/view?request=%7B%22encryptType%22:0,%22data%22:%7B%22studentId%22:{}%7D,%22session%22:%22{}%22,%22datetime%22:1539235776168%7D'.format(
                    studentId1,self.session
                )
                r = requests.get(url,headers=self.headers).text
                data = json.loads(r)
                data = data['data']
                if 'phoneNumber' in data:
                    phoneNumber = data['phoneNumber']
                else:
                    phoneNumber = '空'
                new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
                # 要从第二行开始写，所以这里行数要加1
                self.sheetList[i].write(new_row, 0, studentName1, self.styleContent)
                self.sheetList[i].write(new_row, 1, sex1, self.styleContent)
                self.sheetList[i].write(new_row, 2, gradeName1, self.styleContent)
                self.sheetList[i].write(new_row, 3, className1, self.styleContent)
                self.sheetList[i].write(new_row, 4, individuationUname1, self.styleContent)
                self.sheetList[i].write(new_row, 5, idNumber1, self.styleContent)
                self.sheetList[i].write(new_row, 6, studentCode1, self.styleContent)
                self.sheetList[i].write(new_row, 7, seatNum1, self.styleContent)
                self.sheetList[i].write(new_row, 8, phoneNumber, self.styleContent)
                print('已写入',num+1)
            self.book.save('txt\\天蛙学生信息.xls')
            print(self.classNameList[i], '爬取成功~')
            time.sleep(2)
        # self.book.save('txt\\学生信息.xls')
if __name__ == '__main__':
    g = getStudent()
    g.main()