from random import randint  # 随机函数
from xpinyin import Pinyin
from IQ.base2.initialData import *
from PersonalDemo.pachong.getCountry.read_Xinxi import *
from IQ.base2.className_stu import *
class OnekeyInit:
    '''
    模拟学校信息，一键生成基础2.0一键初始化模板
    '''
    def __init__(self):
        xls = xlrd.open_workbook(r'D:\PythonProject\IQ\base2\基础模板\空\一键初始化模板(空).xls', formatting_info=True)
        self.xlsc = copy(xls)
        self.stuNum = 10
        self.teaNum = 10
        self.parNum = 10
        self.gradeName = '高中'
        if self.gradeName == '小学':
            self.grade, self.classNameList = xiaoxue_Class(10, 'no')
        elif self.gradeName == '初中':
            self.grade, self.classNameList = chuzhong_Class(10, 'no')
        elif self.gradeName == '高中':
            self.grade, self.classNameList = gaozhong_Class(10, 'no')
        elif self.gradeName == '完中':
            self.grade, self.classNameList = wanzhong_Class(10, 'no')
        elif self.gradeName == '九年制':
            self.grade, self.classNameList = jiunianzhi_Class(10, 'no')
        self.gPath = '模拟模板\\一键初始化模板(%s).xls'%self.gradeName
    # 学生模板部分
    def StudentTemplate(self):
        sheet = self.xlsc.get_sheet(0)
        pin = Pinyin()
        allNameList, nPlaceList = read_Num(self.stuNum)
        nameList = Rname(self.stuNum)
        for num in range(self.stuNum):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            Birthday = '%s/%s/%s' % (randint(2000, 2005), randint(1, 12), randint(1, 31))
            B = self.IDTransformation(Birthday)
            Gnum = '{}{}{}'.format(randint(100000, 660000), B, randint(1000, 9999))
            sheet.write(new_row, 0, 'G%s' % Gnum)
            sheet.write(new_row, 1, nameList[num])
            className = self.classNameList[randint(0, len(self.classNameList) - 1)]
            if '年级' in className[0:3]:
                sheet.write(new_row, 7, className[0:3])
                sheet.write(new_row, 8, className[3:])
                sheet.write(new_row, 30, '{}/9/1'.format(self.grade[className[0:3]]))
            else:
                sheet.write(new_row, 7, className[0:2])
                sheet.write(new_row, 8, className[2:])
                sheet.write(new_row, 30, '{}/9/1'.format(self.grade[className[0:2]]))
            sheet.write(new_row, 13, nPlaceList[num])
            sheet.write(new_row, 20, allNameList[num])
            realNamePinyin1 = pin.get_pinyin(nameList[num], "")
            sheet.write(new_row, 4, realNamePinyin1)
            sheet.write(new_row, 2, str(randint(100000000, 999999999)))
            sheet.write(new_row, 3, 'E_' + realNamePinyin1)
            sheet.write(new_row, 5, '曾' + nameList[num])
            if new_row % 2 == 0:
                sheet.write(new_row, 6, '女')
                sheet.write(new_row, 21, '农业户口')
                sheet.write(new_row, 22, '是')
                sheet.write(new_row, 24, '是')
                sheet.write(new_row, 25, '是')
                sheet.write(new_row, 27, '健康')
                sheet.write(new_row, 38, '走读')
                sheet.write(new_row, 39, '是')
                sheet.write(new_row, 40, '是')
            else:
                sheet.write(new_row, 6, '男')
                sheet.write(new_row, 21, '非农户口')
                sheet.write(new_row, 22, '否')
                sheet.write(new_row, 24, '否')
                sheet.write(new_row, 25, '否')
                sheet.write(new_row, 27, '欠佳')
                sheet.write(new_row, 38, '住校')
                sheet.write(new_row, 39, '否')
                sheet.write(new_row, 40, '否')
            sheet.write(new_row, 9, randint(1, 50))
            sheet.write(new_row, 10, Birthday)
            sheet.write(new_row, 17, Gnum)
            sheet.write(new_row, 11, nPlaceList[num])
            sheet.write(new_row, 12, Country[randint(0, len(Country) - 1)])
            sheet.write(new_row, 14, Nation[randint(0, len(Nation) - 1)])
            sheet.write(new_row, 15, Poutlook[randint(0, len(Poutlook) - 1)])
            sheet.write(new_row, 16, Dtype[randint(0, len(Dtype) - 1)])
            sheet.write(new_row, 18, '%s/%s/%s' % (randint(2020, 2040), randint(1, 12), randint(1, 31)))
            sheet.write(new_row, 19, '%s公安局' % nPlaceList[num])
            sheet.write(new_row, 23, allNameList[randint(0, len(allNameList) - 1)])
            sheet.write(new_row, 26, '未婚')
            sheet.write(new_row, 28, Bloodtype[randint(0, len(Bloodtype) - 1)])
            sheet.write(new_row, 29, Religion[randint(0, len(Religion) - 1)])
            sheet.write(new_row, 31, Speciality[randint(0, len(Speciality) - 1)])
            sheet.write(new_row, 32, '%s%s' % (phoneNum[randint(0, len(phoneNum) - 1)], randint(100000000, 999999999)))
            sheet.write(new_row, 33, allNameList[randint(0, len(allNameList) - 1)])
            sheet.write(new_row, 34, randint(100000, 999999))
            qq = randint(100000000, 999999999)
            sheet.write(new_row, 35, '{}@qq.com'.format(qq))
            sheet.write(new_row, 37, '%s' % qq)
            sheet.write(new_row, 36, allNameList[randint(0, len(allNameList) - 1)])
            sheet.write(new_row, 41, '%s' % randint(300, 600))
            sheet.write(new_row, 42, Stutype[randint(0, len(Stutype) - 1)])
            sheet.write(new_row, 43, Schoolname[randint(0, len(Schoolname) - 1)])
            sheet.write(new_row, 44, Gnum)
            sheet.write(new_row, 45, '计算机类')
        self.xlsc.save(self.gPath)
        print('学生数据写入成功,共', self.stuNum, '个学生~~')
    # 老师模板部分
    def TeacherTemplate(self):
        sheet = self.xlsc.get_sheet(1)
        # i既是lis的下标，也代表每一列#处理表头
        pin = Pinyin()
        nameList = Rname(self.teaNum)
        allNameList, nPlaceList = read_Num(self.teaNum)
        # i既是lis的下标，也代表每一列#处理表头
        for num in range(self.teaNum):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, '%s' % randint(100000000, 999999999))
            sheet.write(new_row, 1, nameList[num])
            sheet.write(new_row, 2, '%s%s' % (phoneNum[randint(0, len(phoneNum) - 1)], randint(100000000, 999999999)))
            realNamePinyin1 = pin.get_pinyin(nameList[num], "")
            sheet.write(new_row, 3, 'E_' + realNamePinyin1)
            sheet.write(new_row, 4, realNamePinyin1)
            sheet.write(new_row, 5, '曾' + nameList[num])
            sheet.write(new_row, 6, position[randint(0, len(position) - 1)])
            if new_row % 2 == 0:
                sheet.write(new_row, 7, '女')
                sheet.write(new_row, 16, '是')
                sheet.write(new_row, 17, '已婚')
                sheet.write(new_row, 18, '健康')
            else:
                sheet.write(new_row, 7, '男')
                sheet.write(new_row, 16, '否')
                sheet.write(new_row, 17, '未婚')
                sheet.write(new_row, 18, '欠佳')
            Birthday = '%s/%s/%s' % (randint(1950, 1990), randint(1, 12), randint(1, 31))
            sheet.write(new_row, 8, Birthday)
            sheet.write(new_row, 9, Country[randint(0, len(Country) - 1)])
            sheet.write(new_row, 10, Nplace[randint(0, len(Nplace) - 1)])
            sheet.write(new_row, 11, Nation[randint(0, len(Nation) - 1)])
            sheet.write(new_row, 12, Poutlook[randint(0, len(Poutlook) - 1)])
            sheet.write(new_row, 13, Dtype[randint(0, len(Dtype) - 1)])
            B = self.IDTransformation(Birthday)
            sheet.write(new_row, 14, '%s%s%s' % (randint(200000, 500000), B, randint(1000, 9999)))
            sheet.write(new_row, 15, allNameList[num])
            sheet.write(new_row, 19, Bloodtype[randint(0, len(Bloodtype) - 1)])
            sheet.write(new_row, 20, Religion[randint(0, len(Religion) - 1)])
            sheet.write(new_row, 21, allNameList[randint(0, len(allNameList) - 1)])
            sheet.write(new_row, 22, randint(100000, 999999))
            sheet.write(new_row, 23, '%s@qq.com' % randint(100000000, 999999999))
            sheet.write(new_row, 24, Ptype[randint(0, len(Ptype) - 1)])
            sheet.write(new_row, 25, Otype[randint(0, len(Otype) - 1)])
        self.xlsc.save(self.gPath)
        print('老师数据写入成功,共', self.teaNum, '个老师~~')
    # 老师模板部分，身份证出生日期生成方法
    def IDTransformation(self,Birthday):
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
    # 年级模板部分
    def GradeTemplate(self):
        sheet = self.xlsc.get_sheet(2)
        # i既是lis的下标，也代表每一列#处理表头
        grade_xiaoxue = ['一年级','二年级','三年级','四年级','五年级','六年级']
        grade_chuzhong = ['初一', '初二', '初三']
        grade_gaozhong = ['高一', '高二', '高三']
        if self.gradeName == '小学':
            gradeList = grade_xiaoxue
        elif self.gradeName == '初中':
            gradeList = grade_chuzhong
        else:
            gradeList = grade_gaozhong
        for num in range(len(gradeList)):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, gradeList[num])
            sheet.write(new_row, 1, str(num+1))
        self.xlsc.save(self.gPath)
        print('年级数据写入成功,共', len(gradeList), '个年级~~')
    # 班级模板部分
    def ClassTemplate(self):
        sheet = self.xlsc.get_sheet(3)
        # classNameList =  ['六年级5班', '五年级2班', '四年级2班', '四年级5班', '三年级3班', '三年级6班', '二年级3班', '二年级6班', '一年级2班', '一年级5班', '六年级3班','六年级6班',
        #                   '五年级3班', '四年级3班', '三年级1班', '三年级4班', '二年级1班', '二年级4班', '二年级7班', '一年级3班', '一年级6班', '六年级1班','六年级4班', '五年级1班',
        #                   '四年级1班', '四年级4班', '三年级2班', '三年级5班', '二年级2班', '二年级5班', '一年级1班', '一年级4班', '六年级2班']
        # i既是lis的下标，也代表每一列#处理表头
        for num in range(len(self.classNameList)):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            if '年级' in self.classNameList[num][0:3]:
                sheet.write(new_row, 1, self.classNameList[num][0:3])
                sheet.write(new_row, 0, self.classNameList[num][3:])
                sheet.write(new_row, 2, '{}'.format(self.grade[self.classNameList[num][0:3]]))
            else:
                sheet.write(new_row, 1, self.classNameList[num][0:2])
                sheet.write(new_row, 0, self.classNameList[num][2:])
                sheet.write(new_row, 2, '{}'.format(self.grade[self.classNameList[num][0:2]]))
        self.xlsc.save(self.gPath)
        print('班级数据写入成功,共', len(self.classNameList), '个班级~~')
    # 学年模板部分
    def SemesterYearTemplate(self):
        sheet = self.xlsc.get_sheet(4)
        semesterYearList = ['2017-2018学年','2018-2019学年']
        yearList = ['2017','2018']
        # i既是lis的下标，也代表每一列#处理表头
        for num in range(len(semesterYearList)):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, semesterYearList[num])
            sheet.write(new_row, 1, yearList[num])
        self.xlsc.save(self.gPath)
        print('学年数据写入成功,共', len(semesterYearList), '个学年~~')
    # 学期模板部分
    def SemesterTemplate(self):
        sheet = self.xlsc.get_sheet(5)
        semesterYearList = ['2017-2018学年','2017-2018学年','2018-2019学年','2018-2019学年']
        begin_timeList = ['2017/9/1','2018/3/1','2018/9/1','2019/3/1',]
        end_timeList = ['2018/2/1','2018/6/28','2019/2/1','2019/6/28',]
        StypeList = ['上学期','下学期','上学期','下学期',]
        statusList = ['禁用','禁用','当前学期','禁用',]
        # i既是lis的下标，也代表每一列#处理表头
        for num in range(len(semesterYearList)):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, semesterYearList[num])
            sheet.write(new_row, 1, begin_timeList[num])
            sheet.write(new_row, 2, end_timeList[num])
            sheet.write(new_row, 3, StypeList[num])
            sheet.write(new_row, 4, statusList[num])
        self.xlsc.save(self.gPath)
        print('学期数据写入成功,共', len(semesterYearList), '个学期~~')
    # 作息时间模板部分
    # def SectionTemplate(self):
    #     data = get_Section()
    #     rows = data['rows']
    #     lists = []
    #     if rows:
    #         for row in rows:
    #             dic = {}
    #             no = row['no']
    #             name = row['name']
    #             periodTimeName = row['periodTimeName']
    #             startTime = row['startTime']
    #             startTime = startTime[0:5]
    #             endTime = row['endTime']
    #             endTime = endTime[0:5]
    #             dic['no'] = no
    #             dic['name'] = name
    #             dic['periodTimeName'] = periodTimeName
    #             dic['startTime'] = startTime
    #             dic['endTime'] = endTime
    #             lists.append(dic)
    #         sheet = self.xlsc.get_sheet(6)
    #         # i既是lis的下标，也代表每一列#处理表头
    #         for num in range(len(lists)):
    #             no1 = lists[num]['no']
    #             name1 = lists[num]['name']
    #             periodTimeName1 = lists[num]['periodTimeName']
    #             startTime1 = lists[num]['startTime']
    #             endTime1 = lists[num]['endTime']
    #             new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
    #             # 要从第二行开始写，所以这里行数要加1
    #             sheet.write(new_row, 0, no1)
    #             sheet.write(new_row, 1, name1)
    #             sheet.write(new_row, 2, periodTimeName1)
    #             sheet.write(new_row, 3, startTime1)
    #             sheet.write(new_row, 4, endTime1)
    #         self.xlsc.save(self.gPath)
    #         print('作息时间数据写入成功,一天共', len(lists), '个节次~~')
    #     else:
    #         print('该校没有添加作息时间~')
    # 家长模板部分，该信息为模拟生成
    def ParentTemplate(self):
        sheet = self.xlsc.get_sheet(7)
        nameList = Rname(self.parNum)
        allNameList, nPlaceList = read_Num(self.parNum)
        # i既是lis的下标，也代表每一列#处理表头
        for num in range(self.parNum):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            sheet.write(new_row, 0, nameList[num])
            sheet.write(new_row, 1, '%s%s' % (phoneNum[randint(0, len(phoneNum) - 1)], randint(100000000, 999999999)))
            sheet.write(new_row, 2, Occupation[randint(0, len(Occupation) - 1)])
            sheet.write(new_row, 3, allNameList[num])
            if new_row % 2 == 0:
                sheet.write(new_row, 4, '女')
            else:
                sheet.write(new_row, 4, '男')
            Birthday = '%s/%s/%s' % (randint(1970, 1990), randint(1, 12), randint(1, 31))
            sheet.write(new_row, 5, Birthday)
            sheet.write(new_row, 6, Country[randint(0, len(Country) - 1)])
            sheet.write(new_row, 7, Nation[randint(0, len(Nation) - 1)])
            sheet.write(new_row, 8, Poutlook[randint(0, len(Poutlook) - 1)])
            sheet.write(new_row, 9, allNameList[randint(0, len(allNameList) - 1)])
            sheet.write(new_row, 10, '%s@qq.com' % randint(100000000, 999999999))
        self.xlsc.save(self.gPath)
        print('家长数据模拟写入成功,共', self.parNum, '个家长~~')
    # 建筑模板部分
    # def BuildingTemplate(self):
    #     data = get_Building()
    #     rows = data['rows']
    #     lists = []
    #     if rows:
    #         for row in rows:
    #             dic = {}
    #             buildingName = row['buildingName']
    #             dic['buildingName'] = buildingName
    #             lists.append(dic)
    #         sheet = self.xlsc.get_sheet(8)
    #         # i既是lis的下标，也代表每一列#处理表头
    #         for num in range(len(lists)):
    #             buildingName1 = lists[num]['buildingName']
    #             new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
    #             # 要从第二行开始写，所以这里行数要加1
    #             sheet.write(new_row, 0, buildingName1)
    #             sheet.write(new_row, 1, '教学楼')
    #         self.xlsc.save(self.gPath)
    #         print('建筑数据写入成功,共', len(lists), '栋建筑~~')
    #     else:
    #         print('该校没有添加建筑~')
    # 教室模板部分
    # def ClassroomTemplate(self):
    #     data = get_Classroom()
    #     rows = data['rows']
    #     lists = []
    #     if rows:
    #         for row in rows:
    #             dic = {}
    #             classroomName = row['classroomName']
    #             buildingName = row['buildingName']
    #             capacity = row['capacity']
    #             dic['classroomName'] = classroomName
    #             dic['buildingName'] = buildingName
    #             dic['capacity'] = capacity
    #             lists.append(dic)
    #         sheet = self.xlsc.get_sheet(9)
    #         # i既是lis的下标，也代表每一列#处理表头
    #         for num in range(len(lists)):
    #             classroomName1 = lists[num]['classroomName']
    #             buildingName1 = lists[num]['buildingName']
    #             capacity1 = lists[num]['capacity']
    #             new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
    #             # 要从第二行开始写，所以这里行数要加1
    #             sheet.write(new_row, 0, classroomName1)
    #             sheet.write(new_row, 1, buildingName1)
    #             sheet.write(new_row, 3, '普通教室')
    #             sheet.write(new_row, 4, capacity1)
    #         self.xlsc.save(self.gPath)
    #         print('教室数据写入成功,共', len(lists), '间教室~~')
    #     else:
    #         print('该校没有添加教室~')
if __name__ == '__main__':
    o = OnekeyInit()
    o.StudentTemplate()
    o.TeacherTemplate()
    o.GradeTemplate()
    o.ClassTemplate()
    # o.SemesterYearTemplate()
    # o.SemesterTemplate()
    # o.SectionTemplate()
    o.ParentTemplate()
    # o.BuildingTemplate()
    # o.ClassroomTemplate()