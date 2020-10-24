from random import randint  # 随机函数
import xlrd
from xlutils.copy import copy
from IQ.base2.initialData import *
from xpinyin import Pinyin
from PersonalDemo.pachong.getCountry.read_Xinxi import *
from IQ.base2.className_tea import *
def TeacherTemplate():
    xls = xlrd.open_workbook(r'D:\PythonProject\IQ\base2\基础模板\空\教师模板(空).xls', formatting_info=True)
    xlsc = copy(xls)
    sheet = xlsc.get_sheet(0)
    # i既是lis的下标，也代表每一列#处理表头
    gradeName = '高中'
    subject = ['语文', '数学', '英语']
    max = 3 # 生成多少个老师
    teaNum = 1 # 生成多少个有职位的老师
    teaType = 3 # 生成的老师是什么类型的，3为既是任课老师、也是班主任、年段长，2为在3的类型上随机抽取，1为三种职位只占一种
    isTeaType = False
    pin = Pinyin()
    nameList = Rname(max)
    allNameList, nPlaceList = read_Num(max)
    if gradeName == '小学':
        gradeList,classNameList = tea_xiaoxue_Class(10)
    elif gradeName == '初中':
        gradeList, classNameList = tea_chuzhong_Class(10)
    elif gradeName == '高中':
        gradeList, classNameList = tea_gaozhong_Class(10)
    elif gradeName == '完中':
        gradeList, classNameList = tea_wanzhong_Class(10)
    # elif gradeName == '九年制':
    else:
        gradeList, classNameList = tea_jiunianzhi_Class(10)
    sumList = random.sample(range(1, max), teaNum)
    if teaNum > len(classNameList):
        bzrNum = len(classNameList)
    else:
        bzrNum = teaNum
    banzhurenList = random.sample(range(0, len(classNameList)), bzrNum)
    for num in range(max):
        new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
        # 要从第二行开始写，所以这里行数要加1
        # sheet.write(new_row, 0, '%s'%randint(10000000000000000000, 99999999999999999999))
        sheet.write(new_row, 0, '%s' % randint(100000000, 999999999))
        sheet.write(new_row, 1, nameList[num])
        sheet.write(new_row, 2, '%s%s' % (phoneNum[randint(0, len(phoneNum) - 1)], randint(100000000, 999999999)))
        realNamePinyin1 = pin.get_pinyin(nameList[num], "")

        sheet.write(new_row, 6, '锐达中学')
        sheet.write(new_row, 7, '教研部，语文教研组')

        sheet.write(new_row, 8, 'E_' + realNamePinyin1)
        sheet.write(new_row, 9, realNamePinyin1)
        sheet.write(new_row, 10, '曾' + nameList[num])
        sheet.write(new_row, 11, position[randint(0, len(position) - 1)])
        if new_row % 2 == 0:
            sheet.write(new_row, 12, '女')
            sheet.write(new_row, 21, '是')
            sheet.write(new_row, 22, '已婚')
            sheet.write(new_row, 23, '健康')
        else:
            sheet.write(new_row, 12, '男')
            sheet.write(new_row, 21, '否')
            sheet.write(new_row, 22, '未婚')
            sheet.write(new_row, 23, '欠佳')
        Birthday = '%s/%s/%s' % (randint(1950, 1990), randint(1, 12), randint(1, 31))
        sheet.write(new_row, 13, Birthday)
        sheet.write(new_row, 14, Country[randint(0, len(Country) - 1)])
        sheet.write(new_row, 15, Nplace[randint(0, len(Nplace) - 1)])
        sheet.write(new_row, 16, Nation[randint(0, len(Nation) - 1)])
        sheet.write(new_row, 17, Poutlook[randint(0, len(Poutlook) - 1)])
        sheet.write(new_row, 18, Dtype[randint(0, len(Dtype) - 1)])
        B = IDTransformation(Birthday)
        sheet.write(new_row, 19, '%s%s%s' % (randint(200000, 500000), B, randint(1000, 9999)))
        sheet.write(new_row, 20, allNameList[num])
        sheet.write(new_row, 24, Bloodtype[randint(0, len(Bloodtype) - 1)])
        sheet.write(new_row, 25, Religion[randint(0, len(Religion) - 1)])
        sheet.write(new_row, 26, allNameList[randint(0, len(allNameList) - 1)])
        sheet.write(new_row, 27, randint(100000, 999999))
        sheet.write(new_row, 28, '%s@qq.com' % randint(100000000, 999999999))
        sheet.write(new_row, 29, Ptype[randint(0, len(Ptype) - 1)])
        sheet.write(new_row, 30, Otype[randint(0, len(Otype) - 1)])
        print('已写入',num+1,'条数据~~')
    if isTeaType:
        if teaType == 3:
            for i in range(0,len(sumList)):
                rkInt = randint(1, 4)
                renKe = random.sample(classNameList, rkInt)
                renKeList = []
                for r in renKe:
                    renKeList.append('{}-{}'.format(r,subject[randint(0, len(subject) - 1)]))
                sheet.write(sumList[i], 3, '，'.join(renKeList))
                if i < bzrNum:
                    sheet.write(sumList[i], 4, classNameList[banzhurenList[i]])
                ndInt = randint(1, len(gradeList))
                nianJi = random.sample(gradeList, ndInt)
                sheet.write(sumList[i], 5, '，'.join(nianJi))
        elif teaType == 2:
            for i in range(0,len(sumList)):
                sjNum = randint(1, 3)
                rkInt = randint(1, 4)
                renKe = random.sample(classNameList, rkInt)
                renKeList = []
                for r in renKe:
                    renKeList.append('{}-{}'.format(r,subject[randint(0, len(subject) - 1)]))
                if sjNum == 3:
                    sheet.write(sumList[i], 3, '，'.join(renKeList))
                    if i < bzrNum:
                        sheet.write(sumList[i], 4, classNameList[banzhurenList[i]])
                    ndInt = randint(1, len(gradeList))
                    nianJi = random.sample(gradeList, ndInt)
                    sheet.write(sumList[i], 5, '，'.join(nianJi))
                elif sjNum == 2:
                    sjList = random.sample(range(3,6), 2)
                    for s in sjList:
                        if s == 3:
                            sheet.write(sumList[i], 3, '，'.join(renKeList))
                        elif s == 4:
                            if i < bzrNum:
                                sheet.write(sumList[i], 4, classNameList[banzhurenList[i]])
                        elif s == 5:
                            ndInt = randint(1, len(gradeList))
                            nianJi = random.sample(gradeList, ndInt)
                            sheet.write(sumList[i], 5, '，'.join(nianJi))
                elif sjNum == 1:
                    p_sjNum = randint(3,5)
                    if p_sjNum == 3:
                        sheet.write(sumList[i], 3, '，'.join(renKeList))
                    elif p_sjNum == 4:
                        if i < bzrNum:
                            sheet.write(sumList[i], 4, classNameList[banzhurenList[i]])
                    elif p_sjNum == 5:
                        ndInt = randint(1, len(gradeList))
                        nianJi = random.sample(gradeList, ndInt)
                        sheet.write(sumList[i], 5, '，'.join(nianJi))
        elif teaType == 1:
            pList = range(0, len(sumList)+1, 3)
            for i in range(0,len(pList)-1):
                rkInt = randint(1, 4)
                renKe = random.sample(classNameList, rkInt)
                renKeList = []
                for r in renKe:
                    renKeList.append('{}-{}'.format(r,subject[randint(0, len(subject) - 1)]))
                sheet.write(sumList[pList[i]], 3, '，'.join(renKeList))
                if i < len(banzhurenList):
                    sheet.write(sumList[pList[i]+1], 4, classNameList[banzhurenList[i]])
                ndInt = randint(1, len(gradeList))
                nianJi = random.sample(gradeList, ndInt)
                sheet.write(sumList[pList[i]+2], 5, '，'.join(nianJi))
            if teaNum%3 == 1:
                zhrNum = len(pList)-1
                rkInt = randint(1, 4)
                renKe = random.sample(classNameList, rkInt)
                renKeList = []
                for r in renKe:
                    renKeList.append('{}-{}'.format(r,subject[randint(0, len(subject) - 1)]))
                a_sjNum = randint(3, 5)
                if a_sjNum == 3:
                    sheet.write(sumList[-1], 3, '，'.join(renKeList))
                elif a_sjNum == 4:
                    if zhrNum < len(banzhurenList):
                        sheet.write(sumList[-1], 4, classNameList[banzhurenList[zhrNum]])
                elif a_sjNum == 5:
                    ndInt = randint(1, len(gradeList))
                    nianJi = random.sample(gradeList, ndInt)
                    sheet.write(sumList[-1], 5, '，'.join(nianJi))
            elif teaNum%3 == 2:
                zhrNum = len(pList) - 1
                rkInt = randint(1, 4)
                renKe = random.sample(classNameList, rkInt)
                renKeList = []
                for r in renKe:
                    renKeList.append('{}-{}'.format(r,subject[randint(0, len(subject) - 1)]))
                sList = sumList[-2:]
                for s in range(0, len(sList)):
                    s_sjNum = randint(3, 5)
                    if s_sjNum == 3:
                        sheet.write(sList[s], 3, '，'.join(renKeList))
                    elif s_sjNum == 4:
                        if zhrNum < len(banzhurenList):
                            sheet.write(sList[s], 4, classNameList[banzhurenList[zhrNum]])
                            zhrNum+=1
                    elif s_sjNum == 5:
                        ndInt = randint(1, len(gradeList))
                        nianJi = random.sample(gradeList, ndInt)
                        sheet.write(sList[s], 5, '，'.join(nianJi))
    xlsc.save(r'模拟模板\%s-教师模板(%s)-%s.xls'%(gradeName,str(max),teaNum))
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
TeacherTemplate()