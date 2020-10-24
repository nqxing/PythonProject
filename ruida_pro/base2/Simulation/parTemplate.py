from random import randint  # 随机函数
import xlrd
from xlutils.copy import copy
from IQ.base2.initialData import *
from PersonalDemo.pachong.getCountry.read_Xinxi import *
def ParentTemplate():
    xls = xlrd.open_workbook(r'D:\PythonProject\IQ\base2\基础模板\空\家长模板(空).xls', formatting_info=True)
    xlsc = copy(xls)
    sheet = xlsc.get_sheet(0)
    # i既是lis的下标，也代表每一列#处理表头
    max = 10
    nameList = Rname(max)
    allNameList,nPlaceList = read_Num(max)
    for num in range(max):
        new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
        # 要从第二行开始写，所以这里行数要加1
        sheet.write(new_row, 0, nameList[num])
        sheet.write(new_row, 1, '%s%s' % (phoneNum[randint(0, len(phoneNum) - 1)],randint(100000000, 999999999)))
        sheet.write(new_row, 2, Occupation[randint(0, len(Occupation) - 1)])
        sheet.write(new_row, 3, allNameList[num])
        if new_row%2==0:
            sheet.write(new_row, 4, '女')
        else:
            sheet.write(new_row, 4, '男')
        Birthday = '%s/%s/%s' % (randint(1970,1990),randint(1,12),randint(1,31))
        sheet.write(new_row, 5, Birthday)
        sheet.write(new_row, 6, Country[randint(0, len(Country) - 1)])
        sheet.write(new_row, 7, Nation[randint(0, len(Nation) - 1)])
        sheet.write(new_row, 8, Poutlook[randint(0, len(Poutlook) - 1)])
        sheet.write(new_row, 9, allNameList[randint(0, len(allNameList) - 1)])
        sheet.write(new_row, 10, '%s@qq.com'%randint(100000000, 999999999))
        print('已写入',num+1,'条数据~~')
    xlsc.save(r'模拟模板\家长模板(%s).xls'%max)
ParentTemplate()