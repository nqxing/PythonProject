import xlrd
from xlutils.copy import copy
def xiaoxue_Class(classNum,yes):
    xls = xlrd.open_workbook(r'D:\PythonProject\IQ\base2\基础模板\空\班级模板(空).xls', formatting_info=True)
    xlsc = copy(xls)
    sheet = xlsc.get_sheet(0)
    # grade = {'一年级':'2018', '二年级':'2017', '三年级':'2016', '四年级':'2015', '五年级':'2014', '六年级':'2013'}
    grade = {'一年级':'2019',}
    gradeList = list(grade.keys())
    classNameList = []
    for g in range(len(gradeList)):
        for i in range(classNum):
            classNameList.append('{}{}班'.format(gradeList[g], i + 1))
    if yes == 'yes':
        for num in range(len(classNameList)):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, classNameList[num][3:])
            sheet.write(new_row, 1, classNameList[num][0:3])
            if classNameList[num][0:3] == '六年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            elif classNameList[num][0:3] == '五年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            elif classNameList[num][0:3] == '四年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            elif classNameList[num][0:3] == '三年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            elif classNameList[num][0:3] == '二年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            else:
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
        xlsc.save(r'D:\PythonProject\IQ\base2\Simulation\模拟模板\小学班级模板.xls')
        print('小学班级模板生成成功~~')
    return grade,classNameList

def chuzhong_Class(classNum,yes):
    xls = xlrd.open_workbook(r'D:\PythonProject\IQ\base2\基础模板\空\班级模板(空).xls', formatting_info=True)
    xlsc = copy(xls)
    sheet = xlsc.get_sheet(0)
    grade = {'初一':'2018','初二':'2017','初三':'2016'}
    classNameList = []
    gradeList = list(grade.keys())
    for g in range(len(gradeList)):
        for i in range(classNum):
            classNameList.append('{}{}班'.format(gradeList[g], i + 1))
    if yes == 'yes':
        for num in range(len(classNameList)):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, classNameList[num][2:])
            sheet.write(new_row, 1, classNameList[num][0:2])
            if classNameList[num][0:2] == '初一':
                sheet.write(new_row, 2, grade[classNameList[num][0:2]])
            elif classNameList[num][0:2] == '初二':
                sheet.write(new_row, 2, grade[classNameList[num][0:2]])
            else:
                sheet.write(new_row, 2, grade[classNameList[num][0:2]])
        xlsc.save(r'D:\PythonProject\IQ\base2\Simulation\模拟模板\初中班级模板.xls')
        print('初中班级模板生成成功~~')
    return grade,classNameList

def gaozhong_Class(classNum,yes):
    xls = xlrd.open_workbook(r'D:\PythonProject\IQ\base2\基础模板\空\班级模板(空).xls', formatting_info=True)
    xlsc = copy(xls)
    sheet = xlsc.get_sheet(0)
    grade = {'高一':'2018','高二':'2017','高三':'2016'}
    classNameList = []
    gradeList = list(grade.keys())
    for g in range(len(gradeList)):
        for i in range(classNum):
            classNameList.append('{}{}班'.format(gradeList[g], i + 1))
    if yes == 'yes':
        for num in range(len(classNameList)):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, classNameList[num][2:])
            sheet.write(new_row, 1, classNameList[num][0:2])
            if classNameList[num][0:2] == '高一':
                sheet.write(new_row, 2, grade[classNameList[num][0:2]])
            elif classNameList[num][0:2] == '高二':
                sheet.write(new_row, 2, grade[classNameList[num][0:2]])
            else:
                sheet.write(new_row, 2, grade[classNameList[num][0:2]])
        xlsc.save(r'D:\PythonProject\IQ\base2\Simulation\模拟模板\高中班级模板.xls')
        print('高中班级模板生成成功~~')
    return grade,classNameList

def wanzhong_Class(classNum,yes):
    xls = xlrd.open_workbook(r'D:\PythonProject\IQ\base2\基础模板\空\班级模板(空).xls', formatting_info=True)
    xlsc = copy(xls)
    sheet = xlsc.get_sheet(0)
    grade = {'高一':'2015','高二':'2014','高三':'2013','初一':'2018','初二':'2017','初三':'2016'}
    classNameList = []
    gradeList = list(grade.keys())
    for g in range(len(gradeList)):
        for i in range(classNum):
            classNameList.append('{}{}班'.format(gradeList[g], i + 1))
    if yes == 'yes':
        for num in range(len(classNameList)):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, classNameList[num][2:])
            sheet.write(new_row, 1, classNameList[num][0:2])
            if classNameList[num][0:2] == '高一':
                sheet.write(new_row, 2, grade[classNameList[num][0:2]])
            elif classNameList[num][0:2] == '高二':
                sheet.write(new_row, 2, grade[classNameList[num][0:2]])
            elif classNameList[num][0:2] == '高三':
                sheet.write(new_row, 2, grade[classNameList[num][0:2]])
            elif classNameList[num][0:2] == '初一':
                sheet.write(new_row, 2, grade[classNameList[num][0:2]])
            elif classNameList[num][0:2] == '初二':
                sheet.write(new_row, 2, grade[classNameList[num][0:2]])
            else:
                sheet.write(new_row, 2, grade[classNameList[num][0:2]])
        xlsc.save(r'D:\PythonProject\IQ\base2\Simulation\模拟模板\完中班级模板.xls')
        print('完中班级模板生成成功~~')
    return grade,classNameList

def jiunianzhi_Class(classNum,yes):
    xls = xlrd.open_workbook(r'D:\PythonProject\IQ\base2\基础模板\空\班级模板(空).xls', formatting_info=True)
    xlsc = copy(xls)
    sheet = xlsc.get_sheet(0)
    grade = {'一年级':'2018', '二年级':'2017', '三年级':'2016', '四年级':'2015', '五年级':'2014', '六年级':'2013','七年级':'2012','八年级':'2011','九年级':'2010'}
    gradeList = list(grade.keys())
    classNameList = []
    for g in range(len(gradeList)):
        for i in range(classNum):
            classNameList.append('{}{}班'.format(gradeList[g], i + 1))
    if yes == 'yes':
        for num in range(len(classNameList)):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, classNameList[num][3:])
            sheet.write(new_row, 1, classNameList[num][0:3])
            if classNameList[num][0:3] == '六年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            elif classNameList[num][0:3] == '五年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            elif classNameList[num][0:3] == '四年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            elif classNameList[num][0:3] == '三年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            elif classNameList[num][0:3] == '二年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            elif classNameList[num][0:3] == '七年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            elif classNameList[num][0:3] == '八年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            elif classNameList[num][0:3] == '九年级':
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
            else:
                sheet.write(new_row, 2, grade[classNameList[num][0:3]])
        xlsc.save(r'D:\PythonProject\IQ\base2\Simulation\模拟模板\九年制班级模板.xls')
        print('九年制班级模板生成成功~~')
    return grade,classNameList

# gaozhong_Class(10,'yes')
# chuzhong_Class(10,'yes')
# xiaoxue_Class(10,'yes')
# wanzhong_Class(10,'yes')
# jiunianzhi_Class(10,'yes')
