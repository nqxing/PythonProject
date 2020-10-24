import requests
import re
from hashlib import sha1
import json
import xlwt
def login():
    login_url = 'http://sso.591iq.cn/login?flag=login'
    user_url = 'http://gateway.591iq.cn/base/workbench/build?appId=150636'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    psw = sha1()
    psw.update("123456".encode('utf8'))
    userPwd = psw.hexdigest()
    dict = {
        'userName': 'fqez_admin',
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
    url = 'http://base.591iq.cn/student/student!pageStudent.do'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'Cookie' : 'JSESSIONID=%s; IQ_SSO_Token=%s'%(JSESSIONID,AccessToken)
    }
    data = {
        'rows': 5000,
        'classId': '-1'
    }
    r = requests.post(url,headers=headers,data=data).text
    data = json.loads(r)
    rows = data['rows']
    lists = []
    for row in rows:
        dic = {}
        name = row['name']
        realNamePinyin = row['realNamePinyin']
        gradeName = row['gradeName']
        className = row['className']
        studentNumber = row['studentNumber']
        educationNumber = row['educationNumber']
        createTime = row['createTime']

        dic['name'] = name
        dic['realNamePinyin'] = realNamePinyin
        dic['gradeName'] = gradeName
        dic['className'] = className
        dic['studentNumber'] = studentNumber
        dic['educationNumber'] = educationNumber
        dic['createTime'] = createTime
        lists.append(dic)
    title = ['姓名','拼音','年级','班级','学号','学籍号','录入时间']
    book = xlwt.Workbook()  # 新建一个excel对象
    sheet = book.add_sheet('student')  # 添加一个sheet页
    first_col1 = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
    first_col1.width = 178 * 25
    first_col2 = sheet.col(1)  # xlwt中是行和列都是从0开始计算的
    first_col2.width = 256 * 25
    first_col3 = sheet.col(2)  # xlwt中是行和列都是从0开始计算的
    first_col3.width = 150 * 25
    first_col1 = sheet.col(3)  # xlwt中是行和列都是从0开始计算的
    first_col1.width = 178 * 25
    first_col2 = sheet.col(4)  # xlwt中是行和列都是从0开始计算的
    first_col2.width = 256 * 25
    first_col3 = sheet.col(5)  # xlwt中是行和列都是从0开始计算的
    first_col3.width = 320 * 25
    first_col3 = sheet.col(6)  # xlwt中是行和列都是从0开始计算的
    first_col3.width = 320 * 25
    tall_style = xlwt.easyxf('font: height 360;')  # 36pt,类型小初的字号
    first_row = sheet.row(0)
    first_row.set_style(tall_style)
    styleTitle = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
    al = xlwt.Alignment()
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中
    fnt = xlwt.Font()
    fnt.bold = True
    fnt.name = u'微软雅黑'                # 设置其字体为微软雅黑
    fnt.colour_index = 2
    styleTitle.alignment = al
    styleTitle.font = fnt

    styleContent = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
    styleContent.alignment = al
    for i in range(len(title)):
    # title多长，循环几次
        # sheet.write(0, 0, '文本居中', style)
        sheet.write(0, i, title[i],styleTitle)
    # i既是lis的下标，也代表每一列#处理表头
    for num in range(len(lists)):
        tall_style = xlwt.easyxf('font: height 300;')  # 36pt,类型小初的字号
        first_row = sheet.row(num+1)
        first_row.set_style(tall_style)

        name1 = lists[num]['name']
        realNamePinyin1 = lists[num]['realNamePinyin']
        gradeName1 = lists[num]['gradeName']
        className1 = lists[num]['className']
        studentNumber1 = lists[num]['studentNumber']
        educationNumber1 = lists[num]['educationNumber']
        createTime1 = lists[num]['createTime']
        new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
        # 要从第二行开始写，所以这里行数要加1
        sheet.write(new_row, 0, name1,styleContent)
        sheet.write(new_row, 1, realNamePinyin1,styleContent)
        sheet.write(new_row, 2, gradeName1,styleContent)
        sheet.write(new_row, 3, className1,styleContent)
        sheet.write(new_row, 4, studentNumber1,styleContent)
        sheet.write(new_row, 5, educationNumber1,styleContent)
        sheet.write(new_row, 6, createTime1,styleContent)
        print('已写入',num+1,'条数据~~')
    book.save('txt\\student.xls')
login()