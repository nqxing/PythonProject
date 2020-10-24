import xlwt
import sqlite3
import requests
import time
# 禁用安全请求警告 关闭SSL验证时用
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def addresses(sid, users_id):
    def timeStamp(timeNum):
        timeStamp = float(timeNum / 1000)
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080',
        'cookie': 'SID={}; USERID={};'.format(sid, users_id)
    }
    url = 'https://restapi.ele.me/member/v1/users/{}/addresses?extras[]=is_brand_member'.format(users_id)
    r = requests.get(url, headers=headers, verify=True)
    print(r)
    addresse_list = []
    if r.status_code == 200:
        for j in r.json():
            address_list = []
            address = '{},{}'.format(j['address'], j['address_detail'])
            name = j['name']
            sex = j['sex']
            phone = j['phone']
            created_at = j['created_at']
            created_date = timeStamp(created_at)
            tag = j['tag']
            if sex == 1:
                sex = '先生'
            if sex == 2:
                sex = '女士'
            if sex == 0:
                sex = '未知'
            address_list.append('[{}]{}'.format(tag, address))
            address_list.append('{}'.format(phone))
            address_list.append('{}[{}]'.format(name, sex))
            address_list.append('{}'.format(created_date))
            addresse_list.append(address_list)
        return addresse_list
    else:
        addresse_list.append([r.text, '获取失败', '获取失败', '获取失败'])
        print(addresse_list)
        return addresse_list

book = xlwt.Workbook()  # 新建一个excel对象
sheet = book.add_sheet('地址表')  # 添加一个sheet页
conn = sqlite3.connect(r'C:\Users\Administrator\Desktop\eleme.db')
cursor = conn.cursor()

title = ['微信名', '备注名', '签到手机号', '收货地址', '收货手机', '收货人', '创建时间']
title_style = xlwt.easyxf('font: height 400;')  # 定义标题单元格高度
content_style = xlwt.easyxf('font: height 350;')  # 定义非标题单元格高度
styleTitle = xlwt.XFStyle()  # 创建一个样式对象，初始化样式
styleContent = xlwt.XFStyle()  # 创建一个样式对象，初始化样式

# 设置每一列的宽度
first_col1 = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
first_col1.width = 300 * 25
first_col2 = sheet.col(1)  # xlwt中是行和列都是从0开始计算的
first_col2.width = 300 * 25
first_col3 = sheet.col(2)  # xlwt中是行和列都是从0开始计算的
first_col3.width = 300 * 25
first_col4 = sheet.col(3)  # xlwt中是行和列都是从0开始计算的
first_col4.width = 700 * 25
first_col5 = sheet.col(4)  # xlwt中是行和列都是从0开始计算的
first_col5.width = 300 * 25
first_col6 = sheet.col(5)  # xlwt中是行和列都是从0开始计算的
first_col6.width = 150 * 25
first_col5 = sheet.col(6)  # xlwt中是行和列都是从0开始计算的
first_col5.width = 300 * 25

# 设置应用标题的高度
first_row = sheet.row(0)
first_row.set_style(title_style)
# 设置单元格样式
al = xlwt.Alignment()
al.horz = 0x02  # 设置水平居中
al.vert = 0x01  # 设置垂直居中
fnt = xlwt.Font()
fnt.bold = True  # 字体加粗
fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
fnt.colour_index = 2  # 字体红色

fnt1 = xlwt.Font()
fnt1.name = u'微软雅黑'  # 设置其字体为微软雅黑
# 应用单元格样式
styleTitle.alignment = al
styleTitle.font = fnt

styleContent.alignment = al
styleContent.font = fnt1
for j in range(len(title)):
    # title多长，循环几次
    sheet.write(0, j, title[j], styleTitle)

cursor.execute("select wx_beizhu, wx_name, mobile, sid, users_id from eleme_sign where is_bd = 'yes'")
# cursor.execute("select wx_beizhu, wx_name, mobile, sid, users_id from eleme_sign where id in (1,2,3)")

values = cursor.fetchall()
row = 1
for v in range(len(values)):
    print('------------当前进度{}/{}------------'.format(v+1, len(values)))
    addresse_list = addresses(values[v][3], values[v][4])
    for a in range(len(addresse_list)):
        # 要从第二行开始写，所以这里行数要加1
        first_row = sheet.row(row + a)
        first_row.set_style(content_style)
        sheet.write(row + a, 3, addresse_list[a][0], styleContent)
        sheet.write(row + a, 4, addresse_list[a][1], styleContent)
        sheet.write(row + a, 5, addresse_list[a][2], styleContent)
        sheet.write(row + a, 6, addresse_list[a][3], styleContent)
    sheet.write_merge(row, row + len(addresse_list) - 1, 0, 0, values[v][1], styleContent)
    sheet.write_merge(row, row + len(addresse_list) - 1, 1, 1, values[v][0], styleContent)
    sheet.write_merge(row, row + len(addresse_list) - 1, 2, 2, values[v][2], styleContent)
    row += len(addresse_list)
book.save('地址表.xls')

