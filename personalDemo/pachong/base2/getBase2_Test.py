import requests
import xlwt
class getBase():
    def __init__(self):
        self.log_url = 'http://gateway2-test.591iq.com.cn/apps/base/user/ssoLogin'
        self.sch_url = 'http://gateway2-test.591iq.com.cn/apps/base/school/manager/list'
        self.stu_url = 'http://gateway2-test.591iq.com.cn/apps/base/school/student/list'
        self.tea_url = 'http://gateway2-test.591iq.com.cn/apps/base/school/teacher/list'
        self.par_url = 'http://gateway2-test.591iq.com.cn/apps/base/school/parent/list'
        self.headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
            'AppKey': '02619EF1A99F54F199590E871ED8B9C2'
        }
        self.schDict = {}
        self.stuTitle = ['学生姓名', '性别', '学号', '学籍号', '年级', '班级', '身份证', '座号', '手机号', 'QQ', '家庭住址']
        self.teaTitle = ['教师姓名', '性别', '工号', '手机号']
        self.parTitle = ['家长姓名', '手机号', '孩子姓名']
        self.book = xlwt.Workbook()  # 新建一个excel对象
        self.title_style = xlwt.easyxf('font: height 360;')  # 定义标题单元格高度
        self.content_style = xlwt.easyxf('font: height 300;')  # 定义非标题单元格高度
        self.styleTitle = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
        self.styleContent = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
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
        self.getSchList()
    def getSchList(self):
        dict = {
            'rows': 500,
            'page': 1
        }
        r = requests.post(self.sch_url,headers=self.headers,data=dict).json()
        schList = r['data']['rows']
        for sch in schList:
            tList = []
            schId = sch['id']
            tList.append(sch['fullName'])
            tList.append(sch['simpleName'])
            tList.append(sch['adminName'])
            tList.append(sch['adminPwd'])
            self.schDict[schId] = tList
        with open("txt\\学校信息.txt", "w", encoding='utf-8') as f:
            f.write(str(self.schDict))
        schIdList = list(self.schDict.keys())
        ints = 7
        schIdList1 = [ints]
        for s in range(len(schIdList1)):
            sId = schIdList1[s]
            self.getStu(sId)
            self.getTea(sId)
            self.getPar(sId)
            self.book.save('txt\\%s.xls' % self.schDict[sId][0])
            print('{}/{},{}获取成功~~'.format(s+1,len(schIdList1),self.schDict[sId][0]))
    def getStu(self,sId):
        dict = {
            'rows': 10000,
            'page': 1,
            'schoolId': sId
        }
        r = requests.post(self.stu_url,headers=self.headers,data=dict).json()
        rows = r['data']['rows']
        sheet = self.book.add_sheet('学生')  # 添加一个sheet页
        first_col0 = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
        first_col0.width = 130 * 25
        first_col1 = sheet.col(1)  # xlwt中是行和列都是从0开始计算的
        first_col1.width = 105 * 25
        first_col2 = sheet.col(2)  # xlwt中是行和列都是从0开始计算的
        first_col2.width = 210 * 25
        first_col3 = sheet.col(3)  # xlwt中是行和列都是从0开始计算的
        first_col3.width = 300 * 25
        first_col4 = sheet.col(4)  # xlwt中是行和列都是从0开始计算的
        first_col4.width = 130 * 25
        first_col5 = sheet.col(5)  # xlwt中是行和列都是从0开始计算的
        first_col5.width = 130 * 25
        first_col6 = sheet.col(6)  # xlwt中是行和列都是从0开始计算的
        first_col6.width = 300 * 25
        first_col7 = sheet.col(7)  # xlwt中是行和列都是从0开始计算的
        first_col7.width = 100 * 25
        first_col8 = sheet.col(8)  # xlwt中是行和列都是从0开始计算的
        first_col8.width = 180 * 25
        first_col9 = sheet.col(9)  # xlwt中是行和列都是从0开始计算的
        first_col9.width = 180 * 25
        first_col10 = sheet.col(10)  # xlwt中是行和列都是从0开始计算的
        first_col10.width = 400 * 25
        # 设置应用标题的高度
        first_row = sheet.row(0)
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
        for j in range(len(self.stuTitle)):
            # title多长，循环几次
            sheet.write(0, j, self.stuTitle[j], self.styleTitle)
        for i in range(len(rows)):
            if 'name' in rows[i]:
                stuName = rows[i]['name']
            else:
                stuName = '空'
            if 'sexZh' in rows[i]:
                stuSexZh = rows[i]['sexZh']
            else:
                stuSexZh = '空'
            if 'studentNumber' in rows[i]:
                studentNumber = rows[i]['studentNumber']
            else:
                studentNumber = '空'
            if 'educationNumber' in rows[i]:
                educationNumber = rows[i]['educationNumber']
            else:
                educationNumber = '空'
            if 'gradeName' in rows[i]:
                gradeName = rows[i]['gradeName']
            else:
                gradeName = '空'
            if 'className' in rows[i]:
                className = rows[i]['className']
            else:
                className = '空'
            if 'idCardNumber' in rows[i]:
                idCardNumber = rows[i]['idCardNumber']
                if len(str(idCardNumber)) == 0:
                    idCardNumber = educationNumber[1:len(educationNumber)]
            else:
                if len(educationNumber)==19:
                    idCardNumber = educationNumber[1:len(educationNumber)]
                else:
                    idCardNumber = '空'
            if 'seatNumber' in rows[i]:
                seatNumber = rows[i]['seatNumber']
            else:
                seatNumber = '空'
            if 'mobilePhone' in rows[i]:
                mobilePhone = rows[i]['mobilePhone']
            else:
                mobilePhone = '空'
            if 'qq' in rows[i]:
                qq = rows[i]['qq']
            else:
                qq = '空'
            if 'currentAddress' in rows[i]:
                currentAddress = rows[i]['currentAddress']
            else:
                currentAddress = '空'
            first_row1 = sheet.row(i + 1)
            first_row1.set_style(self.content_style)
            new_row = i + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, stuName, self.styleContent)
            sheet.write(new_row, 1, stuSexZh, self.styleContent)
            sheet.write(new_row, 2, studentNumber, self.styleContent)
            sheet.write(new_row, 3, educationNumber, self.styleContent)
            sheet.write(new_row, 4, gradeName, self.styleContent)
            sheet.write(new_row, 5, className, self.styleContent)
            sheet.write(new_row, 6, idCardNumber, self.styleContent)
            sheet.write(new_row, 7, seatNumber, self.styleContent)
            sheet.write(new_row, 8, mobilePhone, self.styleContent)
            sheet.write(new_row, 9, qq, self.styleContent)
            sheet.write(new_row, 10, currentAddress, self.styleContent)
    def getTea(self,sId):
        dict = {
            'rows': 10000,
            'page': 1,
            'schoolId': sId
        }
        r = requests.post(self.tea_url,headers=self.headers,data=dict).json()
        rows = r['data']['rows']
        sheet = self.book.add_sheet('老师')  # 添加一个sheet页
        first_col0 = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
        first_col0.width = 130 * 25
        first_col1 = sheet.col(1)  # xlwt中是行和列都是从0开始计算的
        first_col1.width = 105 * 25
        first_col2 = sheet.col(2)  # xlwt中是行和列都是从0开始计算的
        first_col2.width = 300 * 25
        first_col3 = sheet.col(3)  # xlwt中是行和列都是从0开始计算的
        first_col3.width = 180 * 25
        # 设置应用标题的高度
        first_row = sheet.row(0)
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
        for j in range(len(self.teaTitle)):
            # title多长，循环几次
            sheet.write(0, j, self.teaTitle[j], self.styleTitle)
        for i in range(len(rows)):
            if 'name' in rows[i]:
                teaName = rows[i]['name']
            else:
                teaName = '空'
            if 'sexZh' in rows[i]:
                teaSexZh = rows[i]['sexZh']
            else:
                teaSexZh = '空'
            if 'workNumber' in rows[i]:
                workNumber = rows[i]['workNumber']
            else:
                workNumber = '空'
            if 'mobilePhone' in rows[i]:
                mobilePhone = rows[i]['mobilePhone']
            else:
                mobilePhone = '空'
            first_row1 = sheet.row(i + 1)
            first_row1.set_style(self.content_style)
            new_row = i + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, teaName, self.styleContent)
            sheet.write(new_row, 1, teaSexZh, self.styleContent)
            sheet.write(new_row, 2, workNumber, self.styleContent)
            sheet.write(new_row, 3, mobilePhone, self.styleContent)
    def getPar(self,sId):
        dict = {
            'rows': 10000,
            'page': 1,
            'schoolId': sId
        }
        r = requests.post(self.par_url,headers=self.headers,data=dict).json()
        rows = r['data']['rows']
        sheet = self.book.add_sheet('家长')  # 添加一个sheet页
        first_col0 = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
        first_col0.width = 160 * 25
        first_col1 = sheet.col(1)  # xlwt中是行和列都是从0开始计算的
        first_col1.width = 180 * 25
        first_col2 = sheet.col(2)  # xlwt中是行和列都是从0开始计算的
        first_col2.width = 180 * 25
        # 设置应用标题的高度
        first_row = sheet.row(0)
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
        for j in range(len(self.parTitle)):
            # title多长，循环几次
            sheet.write(0, j, self.parTitle[j], self.styleTitle)
        for i in range(len(rows)):
            if 'name' in rows[i]:
                parName = rows[i]['name']
            else:
                parName = '无姓名'
            if 'mobilePhone' in rows[i]:
                mobilePhone = rows[i]['mobilePhone']
            else:
                mobilePhone = '空'
            if 'studentList' in rows[i]:
                studentList = rows[i]['studentList']
                if studentList:
                    stuName = []
                    for stu in studentList:
                        stuName.append(stu['name'])
                    studentList = str(stuName)
                else:
                    studentList = '空'
            else:
                studentList = '空'
            first_row1 = sheet.row(i + 1)
            first_row1.set_style(self.content_style)
            new_row = i + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, parName, self.styleContent)
            sheet.write(new_row, 1, mobilePhone, self.styleContent)
            sheet.write(new_row, 2, studentList, self.styleContent)
if __name__ == '__main__':
    o = getBase()
    o.login()