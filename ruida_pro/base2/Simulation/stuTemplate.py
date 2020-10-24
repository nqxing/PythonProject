from random import randint  # 随机函数
from IQ.base2.initialData import *
from PersonalDemo.pachong.getCountry.read_Xinxi import *
from xpinyin import Pinyin
from IQ.base2.className_stu import *
def StudentTemplate():
    xls = xlrd.open_workbook(r'D:\PythonProject\IQ\base2\基础模板\空\学生模板(空).xls', formatting_info=True)
    xlsc = copy(xls)
    sheet = xlsc.get_sheet(0)
    # i既是lis的下标，也代表每一列#处理表头
    pin = Pinyin()
    max = 5
    gradeName = '高中'
    allNameList,nPlaceList = read_Num(max)
    nameList = Rname(max)
    if gradeName == '小学':
        grade,classNameList = xiaoxue_Class(20, 'no')
    elif gradeName == '初中':
        grade, classNameList = chuzhong_Class(10, 'no')
    elif gradeName == '高中':
        grade, classNameList = gaozhong_Class(10, 'yes')
    elif gradeName == '完中':
        grade, classNameList = wanzhong_Class(10, 'no')
    elif gradeName == '九年制':
        grade, classNameList = jiunianzhi_Class(10, 'no')
    for num in range(max):
        new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
        # 要从第二行开始写，所以这里行数要加1
        Birthday = '%s/%s/%s' % (randint(2000, 2005), randint(1, 12), randint(1, 31))
        B = IDTransformation(Birthday)
        Gnum = '{}{}{}'.format(randint(100000,660000),B,randint(1000,9999))
        sheet.write(new_row, 0, 'G%s'%Gnum)
        sheet.write(new_row, 1, nameList[num])
        sheet.write(new_row, 2, str(randint(100000000, 999999999)))
        sheet.write(new_row, 3, str(randint(100000000, 999999999)))
        className = classNameList[randint(0, len(classNameList) - 1)]
        if '年级' in className[0:3]:
            sheet.write(new_row, 5, className[0:3])
            sheet.write(new_row, 6, className[3:])
            sheet.write(new_row, 32, '{}/9/1'.format(grade[className[0:3]]))
        else:
            sheet.write(new_row, 5, className[0:2])
            sheet.write(new_row, 6, className[2:])
            sheet.write(new_row, 32, '{}/9/1'.format(grade[className[0:2]]))
        sheet.write(new_row, 15, nPlaceList[num])
        sheet.write(new_row, 22, allNameList[num])
        realNamePinyin1 = pin.get_pinyin(nameList[num], "")
        sheet.write(new_row, 9, realNamePinyin1)
        sheet.write(new_row, 7, '锐达教学1班-1,锐达教学2班-12')
        sheet.write(new_row, 8, 'E_' + realNamePinyin1)
        sheet.write(new_row, 10, '曾' + nameList[num])
        if new_row % 2 == 0:
            sheet.write(new_row, 4, '女')
            sheet.write(new_row, 23, '农业户口')
            sheet.write(new_row, 24, '是')
            sheet.write(new_row, 26, '是')
            sheet.write(new_row, 27, '是')
            sheet.write(new_row, 29, '健康')
            sheet.write(new_row, 40, '走读')
            sheet.write(new_row, 41, '是')
            sheet.write(new_row, 42, '是')
        else:
            sheet.write(new_row, 4, '男')
            sheet.write(new_row, 23, '非农户口')
            sheet.write(new_row, 24, '否')
            sheet.write(new_row, 26, '否')
            sheet.write(new_row, 27, '否')
            sheet.write(new_row, 29, '欠佳')
            sheet.write(new_row, 40, '住校')
            sheet.write(new_row, 41, '否')
            sheet.write(new_row, 42, '否')
        sheet.write(new_row, 11, randint(1, 50))
        sheet.write(new_row, 12, Birthday)
        sheet.write(new_row, 19, Gnum)
        sheet.write(new_row, 13, nPlaceList[num])
        sheet.write(new_row, 14, Country[randint(0, len(Country) - 1)])
        sheet.write(new_row, 16, Nation[randint(0, len(Nation) - 1)])
        sheet.write(new_row, 17, Poutlook[randint(0, len(Poutlook) - 1)])
        sheet.write(new_row, 18, Dtype[randint(0, len(Dtype) - 1)])
        sheet.write(new_row, 20, '%s/%s/%s' % (randint(2020, 2040), randint(1, 12), randint(1, 31)))
        sheet.write(new_row, 21, '%s公安局' % nPlaceList[num])
        sheet.write(new_row, 25, allNameList[randint(0, len(allNameList) - 1)])
        sheet.write(new_row, 28, '未婚')
        sheet.write(new_row, 30, Bloodtype[randint(0, len(Bloodtype) - 1)])
        sheet.write(new_row, 31, Religion[randint(0, len(Religion) - 1)])
        sheet.write(new_row, 33, Speciality[randint(0, len(Speciality) - 1)])
        sheet.write(new_row, 34, '%s%s' % (phoneNum[randint(0, len(phoneNum) - 1)], randint(100000000, 999999999)))
        sheet.write(new_row, 35, allNameList[randint(0, len(allNameList) - 1)])
        sheet.write(new_row, 36, randint(100000, 999999))
        qq = randint(100000000, 999999999)
        sheet.write(new_row, 37, '{}@qq.com'.format(qq))
        sheet.write(new_row, 39, '%s' % qq)
        sheet.write(new_row, 38, allNameList[randint(0, len(allNameList) - 1)])
        sheet.write(new_row, 43, '%s'%randint(300,600))
        sheet.write(new_row, 44, Stutype[randint(0, len(Stutype) - 1)])
        sheet.write(new_row, 45, Schoolname[randint(0, len(Schoolname) - 1)])
        sheet.write(new_row, 46, Gnum)
        sheet.write(new_row, 47, '计算机类')
        print('已写入',num+1,'条数据~~')
    xlsc.save(r'模拟模板\%s学生模板(%s).xls' % (gradeName, str(max)))
def IDTransformation(Birthday):
    Blist = Birthday.split('/')
    if len(Blist[1]) == 1:
        month = '0%s' % Blist[1]
    else:
        month = Blist[1]
    if len(Blist[2]) == 1:
        day = '0%s' % Blist[2]
    else:
        day = Blist[2]
    return Blist[0] + month + day
StudentTemplate()