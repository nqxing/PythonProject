import requests
import re
from hashlib import sha1
import xlwt
import time

# 正则表达式法获取数据，缺陷：当存在学生年级、班级为空的会缺少字段，会导致匹配的各个数组数量不一致，运行会报错
def login(userName,userPwd):
    login_url = 'http://sso.591iq.cn/login?flag=login'
    user_url = 'http://gateway.591iq.cn/base/workbench/build?appId=150636'
    url = 'http://base.591iq.cn/student/student!pageStudent.do'
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
    headers2 = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'Cookie' : 'JSESSIONID=%s; IQ_SSO_Token=%s'%(JSESSIONID,AccessToken)
    }
    data = {
        'rows': 5000,
        'classId': '-1'
    }
    r = requests.post(url,headers=headers2,data=data).text
    return r
def main():
    f = open("txt\\userdata.txt", "r")
    lines = f.readlines()  # 读取全部内容
    classNameList = []
    userNameList = []
    userPwdList = []
    sheetList = []
    title = ['姓名','拼音','年级','班级','学号','学籍号','录入时间']
    tall_style = xlwt.easyxf('font: height 360;')  # 定义标题单元格高度
    tall_style1 = xlwt.easyxf('font: height 300;')  # 定义非标题单元格高度
    for line in lines:
        userList = line.strip().split(',')
        classNameList.append(userList[0])
        userNameList.append(userList[1])
        userPwdList.append(userList[2])

    book = xlwt.Workbook()  # 新建一个excel对象
    for c in range(len(classNameList)):
        sheetName = book.add_sheet(classNameList[c])  # 添加一个sheet页
        sheetList.append(sheetName)

    for i in range(len(sheetList)):
        # print(sheetList[i])
        first_col1 = sheetList[i].col(0)  # xlwt中是行和列都是从0开始计算的
        first_col1.width = 178 * 25
        first_col2 = sheetList[i].col(1)  # xlwt中是行和列都是从0开始计算的
        first_col2.width = 256 * 25
        first_col3 = sheetList[i].col(2)  # xlwt中是行和列都是从0开始计算的
        first_col3.width = 150 * 25
        first_col4 = sheetList[i].col(3)  # xlwt中是行和列都是从0开始计算的
        first_col4.width = 178 * 25
        first_col5 = sheetList[i].col(4)  # xlwt中是行和列都是从0开始计算的
        first_col5.width = 256 * 25
        first_col6 = sheetList[i].col(5)  # xlwt中是行和列都是从0开始计算的
        first_col6.width = 320 * 25
        first_col7 = sheetList[i].col(6)  # xlwt中是行和列都是从0开始计算的
        first_col7.width = 320 * 25

        first_row = sheetList[i].row(0)
        first_row.set_style(tall_style)

        styleTitle = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        fnt = xlwt.Font()
        fnt.bold = True
        fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
        fnt.colour_index = 2
        styleTitle.alignment = al
        styleTitle.font = fnt

        styleContent = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
        styleContent.alignment = al

        for j in range(len(title)):
            # title多长，循环几次
            sheetList[i].write(0, j, title[j],styleTitle)

        r = login(userNameList[i],userPwdList[i])
        # print(r)

        zz1 = re.compile('"name":"(.*?)"', re.S)
        zz2 = re.compile('"realNamePinyin":"(.*?)"', re.S)
        zz3 = re.compile('"gradeName":"(.*?)"', re.S)
        zz4 = re.compile('"className":"(.*?)"', re.S)
        zz5 = re.compile('"studentNumber":"(.*?)"', re.S)
        zz6 = re.compile('"educationNumber":"(.*?)"', re.S)
        zz7 = re.compile('"createTime":"(.*?)"', re.S)

        nameList = re.findall(zz1, r)
        realNamePinyinList = re.findall(zz2, r)
        gradeNameList = re.findall(zz3, r)
        classNameList = re.findall(zz4, r)
        studentNumberList = re.findall(zz5, r)
        educationNumberList = re.findall(zz6, r)
        createTimeList = re.findall(zz7, r)

        # print(len(nameList))
        # print(len(realNamePinyinList))
        # print(len(gradeNameList))
        # print(len(classNameList))
        # print(len(studentNumberList))
        # print(len(educationNumberList))
        # print(len(createTimeList))

        lists = []
        for n in range(len(nameList)):
            dic = {}
            name = nameList[n]
            realNamePinyin = realNamePinyinList[n]
            gradeName = gradeNameList[n]
            className = classNameList[n]
            studentNumber = studentNumberList[n]
            educationNumber = educationNumberList[n]
            createTime = createTimeList[n]

            dic['name'] = name
            dic['realNamePinyin'] = realNamePinyin
            dic['gradeName'] = gradeName
            dic['className'] = className
            dic['studentNumber'] = studentNumber
            dic['educationNumber'] = educationNumber
            dic['createTime'] = createTime
            lists.append(dic)
        for num in range(len(lists)):

            first_row1 = sheetList[i].row(num + 1)
            first_row1.set_style(tall_style1)

            name1 = lists[num]['name']
            realNamePinyin1 = lists[num]['realNamePinyin']
            gradeName1 = lists[num]['gradeName']
            className1 = lists[num]['className']
            studentNumber1 = lists[num]['studentNumber']
            educationNumber1 = lists[num]['educationNumber']
            createTime1 = lists[num]['createTime']
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheetList[i].write(new_row, 0, name1, styleContent)
            sheetList[i].write(new_row, 1, realNamePinyin1, styleContent)
            sheetList[i].write(new_row, 2, gradeName1, styleContent)
            sheetList[i].write(new_row, 3, className1, styleContent)
            sheetList[i].write(new_row, 4, studentNumber1, styleContent)
            sheetList[i].write(new_row, 5, educationNumber1, styleContent)
            sheetList[i].write(new_row, 6, createTime1, styleContent)
            # print('已写入', num + 1, '条数据~~')
        print('111')
        time.sleep(2)
    book.save('txt\\student.xls')
main()