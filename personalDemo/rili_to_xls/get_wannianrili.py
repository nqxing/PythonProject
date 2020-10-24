# coding=gbk
import requests
from bs4 import BeautifulSoup
import xlwt
# ��ȡһ�����ݣ����ֵ䷵��
def getYear():
    yearDic = {}
    week = 2 # ��ʼ���ڣ�2019��1��1��Ϊ���ڶ�
    year = 2019 # ���
    urlList = []
    uUrl = 'https://wannianrili.51240.com/ajax/?q={}-{}&v=18121803'
    # ����ÿ���µĽӿ�����
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
            # �ҵ���Ԫ����Ϊ�����ڼ���
            if riqi.find_all(class_='wnrl_riqi_xiu'):
                nStr+='(��)'
            dayList.append(week)
            # �������պ�����Ϊ0
            if week == 7:
                week = 0
            week+=1
            dayList.append(gStr)
            dayList.append(nStr)
            monthDic[gStr] = dayList
        yearDic[i+1] = monthDic
    return yearDic,year
# ��ʼÿ���µ����ڱ��ⵥԪ�����꣬ҳ��3*4����ʽչʾ
def coordinates():
    yearCoorDic = {}
    x = 2 # ��ʼ������
    y = 0 # ��ʼ������
    interval = 2 # �·�֮�����������
    for i in range(1,13):
        monthList = []
        # �·�Ϊ1,5,9 ʱnum���³�ʼΪ0
        if i == 1 or i == 5 or i == 9:
            num = y
        if i < 5:
            # ѭ��7�Σ�Ϊ����һ��������
            for k in range(7):
                tList = []
                # cross =  x # ��
                # ÿ��������+1
                column =  k + num # ��
                tList.append(x)
                tList.append(column)
                # ��ס���һ�Σ������죩������+�·ݼ����Ϊ�¸��£�����һ����������ֵ
                if k == 6:
                    num = column+interval
                monthList.append(tList)
        if i>4 and i<9:
            for k in range(7):
                tList = []
                # �����귽��ĵ�Ԫ����������ó���+ũ�����ռ��12�С������14�����Ϻ�������
                cross =  x + 14 # ��
                column =  k + num # ��
                tList.append(cross)
                tList.append(column)
                if k == 6:
                    num = column+interval
                monthList.append(tList)
        if i>8 and i<13:
            for k in range(7):
                tList = []
                cross =  x + 14*2 # ��
                column =  k + num # ��
                tList.append(cross)
                tList.append(column)
                if k == 6:
                    num = column+interval
                monthList.append(tList)
        yearCoorDic[i] = monthList
    return yearCoorDic
def template():
    book = xlwt.Workbook()  # �½�һ��excel����
    sheet = book.add_sheet('������')  # ���һ��sheetҳ
    month_style = xlwt.easyxf('font: height 280;')  # �����·ݱ��ⵥԪ��߶�
    week_style = xlwt.easyxf('font: height 340;')  # �������ڵ�Ԫ��߶�
    Content_style = xlwt.easyxf('font: height 280;') # �������ں�ũ����Ԫ��߶�
    styleRed = xlwt.XFStyle()  # ����һ����ʽ���󣬳�ʼ����ʽ  ��������ĩ��Ԫ��
    styleRed1 = xlwt.XFStyle()  # ����һ����ʽ���󣬳�ʼ����ʽ  ��������ĩ��Ԫ���ҽ���������ʱ
    styleBlack = xlwt.XFStyle()  # ����һ����ʽ���󣬳�ʼ����ʽ �����ڹ����յ�Ԫ��
    styleBlack_ = xlwt.XFStyle()  # ����һ����ʽ���󣬳�ʼ����ʽ ������ũ����Ԫ��
    styleBlack1_ = xlwt.XFStyle() # ����һ����ʽ���󣬳�ʼ����ʽ ������ũ����Ԫ���ҽ���������ʱ
    titleStyle = xlwt.XFStyle()  # ����һ����ʽ���󣬳�ʼ����ʽ  �������·ݱ��ⵥԪ��
    styleContent = xlwt.XFStyle() # ����һ����ʽ���󣬳�ʼ����ʽ  ���������ں�ũ����Ԫ��
    # ���õ�Ԫ����ʽ  ͨ��
    al = xlwt.Alignment()
    al.horz = 0x02  # ����ˮƽ����
    al.vert = 0x01  # ���ô�ֱ����
    # ���õ�Ԫ����ʽ  ������styleRed1 styleBlack1_
    al1 = xlwt.Alignment()
    al1.vert = 0x01  # ���ô�ֱ����
    # ���õ�Ԫ����ʽ  ��������ĩ�ͷ����ڼ���
    fnt = xlwt.Font()
    fnt.bold = True  # ����Ӵ�
    fnt.name = u'΢���ź�'  # ����������Ϊ΢���ź�
    fnt.colour_index = 2  # �����ɫ
    # ���õ�Ԫ����ʽ  �����ڹ����պ�����
    fnt1 = xlwt.Font()
    fnt1.bold = True  # ����Ӵ�
    fnt1.name = u'΢���ź�'  # ����������Ϊ΢���ź�
    fnt1.colour_index = 0  # �����ɫ
    # ���õ�Ԫ����ʽ  ������ũ��
    fnt1_ = xlwt.Font()
    fnt1_.bold = True  # ����Ӵ�
    fnt1_.name = u'΢���ź�'  # ����������Ϊ΢���ź�
    fnt1_.colour_index = 23  # �����ɫ
    # ���õ�Ԫ����ʽ  �������·ݱ�����ʾ
    fnt2 = xlwt.Font()
    fnt2.bold = True  # ����Ӵ�
    fnt2.name = u'΢���ź�'  # ����������Ϊ΢���ź�
    fnt2.colour_index = 1  # �����ɫ
    pattern = xlwt.Pattern()  # Create the pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern.pattern_fore_colour = 8  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on..
    # Ӧ�õ�Ԫ����ʽ
    styleRed.alignment = al
    styleRed.font = fnt
    styleRed1.alignment = al1
    styleRed1.font = fnt
    # Ӧ�õ�Ԫ����ʽ
    styleBlack.alignment = al
    styleBlack.font = fnt1
    # Ӧ�õ�Ԫ����ʽ
    styleBlack_.alignment = al
    styleBlack_.font = fnt1_
    styleBlack1_.alignment = al1
    styleBlack1_.font = fnt1_
    # Ӧ�õ�Ԫ����ʽ
    titleStyle.alignment = al
    titleStyle.font = fnt2
    titleStyle.pattern = pattern
    styleContent.alignment = al
    # ��ȡÿ�������ڱ��������ʼֵ
    yearCoorDic = coordinates()
    print('���ڻ�ȡ��������...')
    # ��ȡһ�������
    yearDic, year = getYear()
    titList = list(yearCoorDic.keys())
    print('%s�����ݻ�ȡ�ɹ�,����д��ģ��...' % year)
    for i in range(len(titList)):  # 12���·�
        # ��ȡ��һ���·ݵ����ڳ�ʼ����
        titcoorList = yearCoorDic[titList[i]]
        # ����Ӧ���·ݱ���ĸ߶�
        first_row = sheet.row(titcoorList[0][0]-1)
        first_row.set_style(month_style)
        sheet.write_merge(titcoorList[0][0]-1, titcoorList[0][0]-1, titcoorList[0][1], titcoorList[-1][1], '{}��'.format(i+1), titleStyle)  # �ϲ���Ԫ��д���·�
        # ��������д�����ڱ���
        for j in range(0,len(titcoorList)):
            # ����Ӧ�����ڱ�����
            first_col = sheet.col(titcoorList[j][1])
            first_col.width = 95 * 25
            # ����Ӧ�����ڱ���ĸ߶�
            first_row = sheet.row(titcoorList[j][0])
            first_row.set_style(week_style)
            if j+1 == 1:
                title = '����һ'
            elif j+1 == 2:
                title = '���ڶ�'
            elif j+1 == 3:
                title = '������'
            elif j+1 == 4:
                title = '������'
            elif j+1 == 5:
                title = '������'
            elif j+1 == 6:
                title = '������'
            else:
                title = '������'
            sheet.write(titcoorList[j][0], titcoorList[j][1], title , styleBlack if j+1<6 else styleRed)
        # ��ʼÿ�����ں������ʼֵ
        oneNum, twoNum, threeNum, fourNum, fiveNum, sixNum, sevenNum = 1, 1, 1, 1, 1, 1, 1 # �ܾ����м򻯵ķ��� ����д�о���ɵ-.-
        # ��ȡ��һ���·����ݵļ�ֵ�б�
        daykeyList = list(yearDic[titList[i]].keys())
        for k in range(len(daykeyList)): # ÿ���µ�����
            dayList = yearDic[titList[i]][daykeyList[k]] # ��ȡÿ�յ��б�ֵ['2','01','Ԫ��']  ��һ��ֵΪ���ڼ����ڶ���Ϊ���ڣ�������Ϊũ����ڼ���
            # �ж�ÿ���µ�һ��Ϊ���ڼ�����Ϊ���ڶ����������һ�ĺ������ʼֵ��ʼΪ3��������һΪ�գ��Դ�����
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
            # �ж����������ڼ���ִ�ж�Ӧ���
            if 1 == dayList[0]:
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[0][0] + oneNum)
                first_row.set_style(Content_style)
                # д�����ڣ����ں������ֵΪ��ʼ���ڱ�������ֵ+oneNum��ʼֵ
                sheet.write(titcoorList[0][0] + oneNum, titcoorList[0][1], dayList[1], styleRed if '��' in dayList[2] else  styleBlack)
                # ��ʼֵ+1 Ϊ�¸�ũ���ڼ��յĳ�ʼֵ
                oneNum+=1
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[0][0] + oneNum)
                first_row.set_style(Content_style)
                # д��ũ����ڼ��� ��ʼ���ڱ���+oneNum��ʼֵ
                sheet.write(titcoorList[0][0] + oneNum, titcoorList[0][1], dayList[2], styleRed if '��' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                oneNum+=1
            if 2 == dayList[0]:
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[1][0] + twoNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[1][0] + twoNum, titcoorList[1][1], dayList[1], styleRed if '��' in dayList[2] else  styleBlack)
                twoNum+=1
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[1][0] + twoNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[1][0] + twoNum, titcoorList[1][1], dayList[2], styleRed if '��' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                twoNum+=1
            if 3 == dayList[0]:
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[2][0] + threeNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[2][0] + threeNum, titcoorList[2][1], dayList[1], styleRed if '��' in dayList[2] else  styleBlack)
                threeNum+=1
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[2][0] + threeNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[2][0] + threeNum, titcoorList[2][1], dayList[2], styleRed if '��' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                threeNum+=1
            if 4 == dayList[0]:
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[3][0] + fourNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[3][0] + fourNum, titcoorList[3][1], dayList[1], styleRed if '��' in dayList[2] else  styleBlack)
                fourNum+=1
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[3][0] + fourNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[3][0] + fourNum, titcoorList[3][1], dayList[2], styleRed if '��' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                fourNum+=1
            if 5 == dayList[0]:
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[4][0] + fiveNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[4][0] + fiveNum, titcoorList[4][1], dayList[1], styleRed if '��' in dayList[2] else  styleBlack)
                fiveNum+=1
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[4][0] + fiveNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[4][0] + fiveNum, titcoorList[4][1], dayList[2], styleRed if '��' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                fiveNum+=1
            if 6 == dayList[0]:
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[5][0] + sixNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[5][0] + sixNum, titcoorList[5][1], dayList[1], styleRed)
                sixNum+=1
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[5][0] + sixNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[5][0] + sixNum, titcoorList[5][1], dayList[2], styleRed if '��' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                sixNum+=1
            if 7 == dayList[0]:
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[6][0] + sevenNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[6][0] + sevenNum, titcoorList[6][1], dayList[1], styleRed)
                sevenNum+=1
                # ����Ӧ�õ�Ԫ��ĸ߶�
                first_row = sheet.row(titcoorList[6][0] + sevenNum)
                first_row.set_style(Content_style)
                sheet.write(titcoorList[6][0] + sevenNum, titcoorList[6][1], dayList[2], styleRed if '��' in dayList[2] else  styleBlack1_ if len(dayList[2])>4 else styleBlack_)
                sevenNum+=1
    book.save('%s��������.xls'%year)
    print('����ɹ�,����ִ�����...')
template()