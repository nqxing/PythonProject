# coding=gbk
import requests
from bs4 import BeautifulSoup
import xlwt
# 获取一年数据，以字典返回
def getYear():
    yearDic = {}
    week = 2 # 初始星期，2019年1月1日为星期二
    year = 2019 # 年份
    urlList = []
    uUrl = 'https://wannianrili.51240.com/ajax/?q={}-{}&v=18121803'
    # 构造每个月的接口链接
    for y in range(1,13):
        if y<10:
            rUrl = uUrl.format(year,'0'+str(y))
            urlList.append(rUrl)
        else:
            rUrl = uUrl.format(year,y)
            urlList.append(rUrl)
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    for i in range(0,len(urlList)):
        monthDic = {}
        html = requests.get(urlList[i], headers=headers)
        soup = BeautifulSoup(html.content, 'lxml')
        riqiList = soup.find_all(class_='wnrl_riqi')
        for riqi in riqiList:
            dayList = []
            g = riqi.find_all(class_='wnrl_td_gl')
            n = riqi.find_all(class_='wnrl_td_bzl')
            gStr = g[0].get_text()
            nStr = n[0].get_text()
            # 找到该元素视为法定节假日
            if riqi.find_all(class_='wnrl_riqi_xiu'):
                nStr+='(休)'
            dayList.append(week)
            # 到星期日后重置为0
            if week == 7:
                week = 0
            week+=1
            dayList.append(gStr)
            dayList.append(nStr)
            monthDic[gStr] = dayList
        yearDic[i+1] = monthDic
    return yearDic,year
# 初始每个月的星期标题单元格坐标，页面3*4网格方式展示
def coordinates():
    yearCoorDic = {}
    x = 2 # 初始横坐标
    y = 0 # 初始纵坐标
    interval = 2 # 月份之间的纵坐标间距
    for i in range(1,13):
        monthList = []
        # 月份为1,5,9 时num重新初始为0
        if i == 1 or i == 5 or i == 9:
            num = y
        if i < 5:
            # 循环7次，为星期一到星期天
            for k in range(7):
                tList = []
                # cross =  x # 横
                # 每次纵坐标+1
                column =  k + num # 纵
                tList.append(x)
                tList.append(column)
                # 记住最后一次（星期天）纵坐标+月份间隔，为下个月（星期一）的纵坐标值
                if k == 6:
                    num = column+interval
                monthList.append(tList)
        if i>4 and i<9:
            for k in range(7):
                tList = []
                # 横坐标方向的单元格数，计算得出日+农历最大占用12行。这里给14行算上横坐标间距
                cross =  x + 14 # 横
                column =  k + num # 纵
                tList.append(cross)
                tList.append(column)
                if k == 6:
                    num = column+interval
                monthList.append(tList)
        if i>8 and i<13:
            for k in range(7):
                tList = []
                cross =  x + 14*2 # 横
                column =  k + num # 纵
                tList.append(cross)
                tList.append(column)
                if k == 6:
                    num = column+interval
                monthList.append(tList)
        yearCoorDic[i] = monthList
    return yearCoorDic
def template():
    book = xlwt.Workbook()  # 新建一个excel对象
    sheet = book.add_sheet('日历表')  # 添加一个sheet页
    month_style = xlwt.easyxf('font: height 280;')  # 定义月份标题单元格高度
    week_style = xlwt.easyxf('font: height 340;')  # 定义星期单元格高度
    Content_style = xlwt.easyxf('font: height 280;') # 定义日期和农历单元格高度
    styleRed = xlwt.XFStyle()  # 创建一个样式对象，初始化样式  适用于周末单元格
    styleRed1 = xlwt.XFStyle()  # 创建一个样式对象，初始化样式  适用于周末单元格且节日名过长时
    styleBlack = xlwt.XFStyle()  # 创建一个样式对象，初始化样式 适用于工作日单元格
    styleBlack_ = xlwt.XFStyle()  # 创建一个样式对象，初始化样式 适用于农历单元格
    styleBlack1_ = xlwt.XFStyle() # 创建一个样式对象，初始化样式 适用于农历单元格且节日名过长时
    titleStyle = xlwt.XFStyle()  # 创建一个样式对象，初始化样式  适用于月份标题单元格
    styleContent = xlwt.XFStyle() # 创建一个样式对象，初始化样式  适用于日期和农历单元格
    # 设置单元格样式  通用
    al = xlwt.Alignment()
    al.horz = 0x02  # 设置水平居中
    al.vert = 0x01  # 设置垂直居中
    # 设置单元格样式  适用于styleRed1 styleBlack1_
    al1 = xlwt.Alignment()
    al1.vert = 0x01  # 设置垂直居中
    # 设置单元格样式  适用于周末和法定节假日
    fnt = xlwt.Font()
    fnt.bold = True  # 字体加粗
    fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
    fnt.colour_index = 2  # 字体红色
    # 设置单元格样式  适用于工作日和星期
    fnt1 = xlwt.Font()
    fnt1.bold = True  # 字体加粗
    fnt1.name = u'微软雅黑'  # 设置其字体为微软雅黑
    fnt1.colour_index = 0  # 字体黑色
    # 设置单元格样式  适用于农历
    fnt1_ = xlwt.Font()
    fnt1_.bold = True  # 字体加粗
    fnt1_.name = u'微软雅黑'  # 设置其字体为微软雅黑
    fnt1_.colour_index = 23  # 字体灰色
    # 设置单元格样式  适用于月份标题显示
    fnt2 = xlwt.Font()
    fnt2.bold = True  # 字体加粗
    fnt2.name = u'微软雅黑'  # 设置其字体为微软雅黑
    fnt2.colour_index = 1  # 字体黑色
    pattern = xlwt.Pattern()  # Create the pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern.pattern_fore_colour = 8  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on..
    # 应用单元格样式
    styleRed.alignment = al
    styleRed.font = fnt
    styleRed1.alignment = al1
    styleRed1.font = fnt
    # 应用单元格样式
    styleBlack.alignment = al
    styleBlack.font = fnt1
    # 应用单元格样式
    styleBlack_.alignment = al
    styleBlack_.font = fnt1_
    styleBlack1_.alignment = al1
    styleBlack1_.font = fnt1_
    # 应用单元格样式
    titleStyle.alignment = al
    titleStyle.font = fnt2
    titleStyle.pattern = pattern
    styleContent.alignment = al
    # 获取每个月星期标题坐标初始值
    yearCoorDic = coordinates()
    print('正在获取日历数据...')
    # 获取一年的数据
    yearDic, year = getYear()
    titList = list(yearCoorDic.keys())
    print('%s年数据获取成功,正在写入模板...' % year)
    for i in range(len(titList)):  # 12个月份
        # 获取第一个月份的星期初始坐标
        titcoorList = yearCoorDic[titList[i]]
        # 设置应用月份标题的高度
        first_row = sheet.row(titcoorList[0][0]-1)
        first_row.set_style(month_style)
        sheet.write_merge(titcoorList[0][0]-1, titcoorList[0][0]-1, titcoorList[0][1], titcoorList[-1][1], '{}月'.format(i+1), titleStyle)  # 合并单元格并写入月份
        # 根据坐标写入星期标题
        for j in range(0,len(titcoorList)):
            # 设置应用星期标题宽度
            first_col = sheet.col(titcoorList[j][1])
            first_col.width = 95 * 25
            # 设置应用星期标题的高度
            first_row = sheet.row(titcoorList[j][0])
            first_row.set_style(week_style)
            if j+1 == 1:
                title = '星期一'
            elif j+1 == 2:
                title = '星期二'
            elif j+1 == 3:
                title = '星期三'
            elif j+1 == 4:
                title = '星期四'
            elif j+1 == 5:
                title = '星期五'
            elif j+1 == 6:
                title = '星期六'
            else:
                title = '星期日'
            sheet.write(titcoorList[j][0], titcoorList[j][1], title , styleBlack if j+1<6 else styleRed)
        # 初始每个星期横坐标初始值
        oneNum, twoNum, threeNum, fourNum, fiveNum, sixNum, sevenNum = 1, 1, 1, 1, 1, 1, 1 # 总觉得有简化的方法 这样写感觉好傻-.-
        # 获取第一个月份数据的键值列表
        daykeyList = list(yearDic[titList[i]].keys())
        for k in range(len(daykeyList)): # 每个月的日期
            dayList = yearDic[titList[i]][daykeyList[k]] # 获取每日的列表值['2','01','元旦']  第一个值为星期几，第二个为日期，第三个为农历或节假日
            # 判断每个月第一天为星期几，若为星期二，则把星期一的横坐标初始值初始为3，即星期一为空，以此类推
            if k == 0:
                if dayList[0]==2:
                    oneNum = 3
                if dayList[0]==3:
                    oneNum,twoNum = 3,3
                if dayList[0]==4:
                    oneNum,twoNum,threeNum = 3,3,3
                if dayList[0]==5:
                    oneNum,twoNum,threeNum,fourNum= 3,3,3,3
                if dayList[0]==6:
                    oneNum,twoNum,threeNum,fourNum,fiveNum= 3,3,3,3,3
                if dayList[0]==7:
                    oneNum,twoNum,threeNum,fourNum,fiveNum,sixNum= 3,3,3,3,3,3
            # 判断日期是星期几，执行对应语句
            if 1 == dayList[0]:
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[0][0] + oneNum)
                first_row.set_style(Content_style)
                # 写入日期，日期横坐标的值为初始星期标题坐标值+oneNum初始值
                sheet.write(titcoorList[0][0] + oneNum, titcoorList[0][1], dayList[1], styleRed if '休' in dayList[2] else  styleBlack)
                # 初始值+1 为下个农历节假日的初始值
                oneNum+=1
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[0][0] + oneNum)
                first_row.set_style(Content_style)
                # 写入农历或节假日 初始星期标题+oneNum初始值
                sheet.write(titcoorList[0][0] + oneNum, titcoorList[0][1], dayList[2], styleRed if '休' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                oneNum+=1
            if 2 == dayList[0]:
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[1][0] + twoNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[1][0] + twoNum, titcoorList[1][1], dayList[1], styleRed if '休' in dayList[2] else  styleBlack)
                twoNum+=1
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[1][0] + twoNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[1][0] + twoNum, titcoorList[1][1], dayList[2], styleRed if '休' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                twoNum+=1
            if 3 == dayList[0]:
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[2][0] + threeNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[2][0] + threeNum, titcoorList[2][1], dayList[1], styleRed if '休' in dayList[2] else  styleBlack)
                threeNum+=1
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[2][0] + threeNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[2][0] + threeNum, titcoorList[2][1], dayList[2], styleRed if '休' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                threeNum+=1
            if 4 == dayList[0]:
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[3][0] + fourNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[3][0] + fourNum, titcoorList[3][1], dayList[1], styleRed if '休' in dayList[2] else  styleBlack)
                fourNum+=1
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[3][0] + fourNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[3][0] + fourNum, titcoorList[3][1], dayList[2], styleRed if '休' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                fourNum+=1
            if 5 == dayList[0]:
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[4][0] + fiveNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[4][0] + fiveNum, titcoorList[4][1], dayList[1], styleRed if '休' in dayList[2] else  styleBlack)
                fiveNum+=1
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[4][0] + fiveNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[4][0] + fiveNum, titcoorList[4][1], dayList[2], styleRed if '休' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                fiveNum+=1
            if 6 == dayList[0]:
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[5][0] + sixNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[5][0] + sixNum, titcoorList[5][1], dayList[1], styleRed)
                sixNum+=1
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[5][0] + sixNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[5][0] + sixNum, titcoorList[5][1], dayList[2], styleRed if '休' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                sixNum+=1
            if 7 == dayList[0]:
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[6][0] + sevenNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[6][0] + sevenNum, titcoorList[6][1], dayList[1], styleRed)
                sevenNum+=1
                # 设置应用单元格的高度
                first_row = sheet.row(titcoorList[6][0] + sevenNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[6][0] + sevenNum, titcoorList[6][1], dayList[2], styleRed if '休' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                sevenNum+=1
    book.save('%s年日历表.xls'%year)
    print('保存成功,程序执行完毕...')
template()