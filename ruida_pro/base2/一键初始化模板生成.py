from random import randint  # 随机函数
from xpinyin import Pinyin
import xlrd
from xlutils.copy import copy
from IQ.base2.initialData import *
from IQ.base2.iqBaseDef import *
from PersonalDemo.pachong.getCountry.read_Xinxi import *
class OnekeyInit:
    '''
    根据多学校平台学校现存信息，一键生成基础2.0一键初始化模板
    '''
    def __init__(self):
        xls = xlrd.open_workbook(r'基础模板\空\一键初始化模板(空).xls', formatting_info=True)
        self.xlsc = copy(xls)
        name = get_SchName()
        schPath = r"基础模板\%s" % name
        folder = os.path.exists(schPath)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(schPath)  # makedirs 创建文件时如果路径不存在会创建这个路径
        self.gPath = '%s\\一键初始化模板.xls'%schPath
    # 学生模板部分
    def StudentTemplate(self):
        data = get_Student()
        rows = data['rows']
        lists = []
        if rows:
            for row in rows:
                dic = {}
                if 'name' in row:
                    name = row['name']
                else:
                    name = '空'
                if 'realNamePinyin' in row:
                    realNamePinyin = row['realNamePinyin']
                else:
                    realNamePinyin = '空'
                if 'gradeName' in row:
                    gradeName = row['gradeName']
                else:
                    gradeName = '空'
                if 'className' in row:
                    className = row['className']
                else:
                    className = '空'
                if 'studentNumber' in row:
                    studentNumber = row['studentNumber']
                else:
                    studentNumber = '空'
                if 'educationNumber' in row:
                    educationNumber = row['educationNumber']
                else:
                    educationNumber = '空'
                dic['name'] = name
                dic['realNamePinyin'] = realNamePinyin
                dic['gradeName'] = gradeName
                dic['className'] = className
                dic['studentNumber'] = studentNumber
                dic['educationNumber'] = educationNumber
                lists.append(dic)
            sheet = self.xlsc.get_sheet(0)
            allNameList, nPlaceList = read_Num(len(lists))
            for num in range(len(lists)):
                name1 = lists[num]['name']
                realNamePinyin1 = lists[num]['realNamePinyin']
                gradeName1 = lists[num]['gradeName']
                className1 = lists[num]['className']
                studentNumber1 = lists[num]['studentNumber']
                educationNumber1 = lists[num]['educationNumber']
                new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
                # 要从第二行开始写，所以这里行数要加1
                sheet.write(new_row, 2, name1)
                sheet.write(new_row, 4, realNamePinyin1)
                sheet.write(new_row, 7, gradeName1)
                sheet.write(new_row, 8, className1)
                sheet.write(new_row, 1, studentNumber1)
                sheet.write(new_row, 0, educationNumber1)
                sheet.write(new_row, 3, 'E_' + realNamePinyin1)
                sheet.write(new_row, 5, '曾' + name1)
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
                if len(educationNumber1) == 19:
                    year = educationNumber1[7:11]
                    month = educationNumber1[11:13]
                    day = educationNumber1[13:15]
                    sheet.write(new_row, 10, '%s/%s/%s' % (year, month, day))
                    sheet.write(new_row, 17, educationNumber1[-18:])
                else:
                    sheet.write(new_row, 10, '2000/11/11')
                    sheet.write(new_row, 17, studentNumber1)
                sheet.write(new_row, 11, nPlaceList[num])
                sheet.write(new_row, 12, Country[randint(0, len(Country) - 1)])
                sheet.write(new_row, 13, nPlaceList[num])
                sheet.write(new_row, 14, Nation[randint(0, len(Nation) - 1)])
                sheet.write(new_row, 15, Poutlook[randint(0, len(Poutlook) - 1)])
                sheet.write(new_row, 16, Dtype[randint(0, len(Dtype) - 1)])
                sheet.write(new_row, 18, '%s/%s/%s' % (randint(2020, 2040), randint(1, 12), randint(1, 31)))
                sheet.write(new_row, 19, '%s公安局' % nPlaceList[num])
                sheet.write(new_row, 20, allNameList[num])
                sheet.write(new_row, 23, allNameList[randint(0, len(allNameList) - 1)])
                sheet.write(new_row, 26, '未婚')
                sheet.write(new_row, 28, Bloodtype[randint(0, len(Bloodtype) - 1)])
                sheet.write(new_row, 29, Religion[randint(0, len(Religion) - 1)])
                if gradeName1 == '高一':
                    sheet.write(new_row, 30, '2018/9/1')
                else:
                    sheet.write(new_row, 30, '2017/9/1')
                sheet.write(new_row, 31, Speciality[randint(0, len(Speciality) - 1)])
                sheet.write(new_row, 32,
                            '%s%s' % (phoneNum[randint(0, len(phoneNum) - 1)], randint(100000000, 999999999)))
                sheet.write(new_row, 33, allNameList[randint(0, len(allNameList) - 1)])
                sheet.write(new_row, 34, randint(100000, 999999))
                qq = randint(100000000, 999999999)
                sheet.write(new_row, 35, '{}@qq.com'.format(qq))
                sheet.write(new_row, 37, '%s' % qq)
                sheet.write(new_row, 36, allNameList[randint(0, len(allNameList) - 1)])
                sheet.write(new_row, 41, educationNumber1[1:4])
                sheet.write(new_row, 42, Stutype[randint(0, len(Stutype) - 1)])
                sheet.write(new_row, 43, Schoolname[randint(0, len(Schoolname) - 1)])
                sheet.write(new_row, 44, educationNumber1)
                sheet.write(new_row, 45, '计算机类')
            self.xlsc.save(self.gPath)
            print('学生数据写入成功,共', len(lists), '个学生~~')
        else:
            print('该校没有学生~')
    # 老师模板部分
    def TeacherTemplate(self):
        data = get_Teacher()
        rows = data['rows']
        lists = []
        if rows:
            for row in rows:
                dic = {}
                if 'realName' in row:
                    name = row['realName']
                else:
                    name = '空'
                if 'workNumber' in row:
                    educationNumber = row['workNumber']
                else:
                    educationNumber = '空'
                dic['name'] = name
                dic['educationNumber'] = educationNumber
                lists.append(dic)
            sheet = self.xlsc.get_sheet(1)
            pin = Pinyin()
            # i既是lis的下标，也代表每一列#处理表头
            for num in range(len(lists)):
                name1 = lists[num]['name']
                educationNumber1 = lists[num]['educationNumber']
                new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
                # 要从第二行开始写，所以这里行数要加1
                sheet.write(new_row, 1, name1)
                sheet.write(new_row, 0, educationNumber1)
                sheet.write(new_row, 2, '%s%s' % (phoneNum[randint(0, len(phoneNum) - 1)], randint(100000000, 999999999)))
                realNamePinyin1 = pin.get_pinyin(name1, "")
                sheet.write(new_row, 3, 'E_' + realNamePinyin1)
                sheet.write(new_row, 4, realNamePinyin1)
                sheet.write(new_row, 5, '曾' + name1)
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
                sheet.write(new_row, 15, '%s%s区%s栋%s楼%s号' % (
                Nplace[randint(0, len(Nplace) - 1)], GBK2312(randint(2, 4)), randint(1, 30), randint(1, 33),
                randint(1000, 9999)))
                sheet.write(new_row, 19, Bloodtype[randint(0, len(Bloodtype) - 1)])
                sheet.write(new_row, 20, Religion[randint(0, len(Religion) - 1)])
                sheet.write(new_row, 21, '%s%s区%s路%s号' % (
                Nplace[randint(0, len(Nplace) - 1)], GBK2312(randint(2, 4)), GBK2312(randint(2, 4)), randint(100, 999)))
                sheet.write(new_row, 22, randint(100000, 999999))
                sheet.write(new_row, 23, '%s@qq.com' % randint(100000000, 999999999))
                sheet.write(new_row, 24, Ptype[randint(0, len(Ptype) - 1)])
                sheet.write(new_row, 25, Otype[randint(0, len(Otype) - 1)])
            self.xlsc.save(self.gPath)
            print('老师数据写入成功,共', len(lists), '个老师~~')
        else:
            print('该校没有老师~')
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
        data = get_Grade()
        rows = data['rows']
        lists = []
        if rows:
            for row in rows:
                dic = {}
                gradeName = row['gradeName']
                sorts = row['sorts']
                dic['gradeName'] = gradeName
                dic['sorts'] = sorts
                lists.append(dic)
            sheet = self.xlsc.get_sheet(2)
            # i既是lis的下标，也代表每一列#处理表头
            for num in range(len(lists)):
                gradeName1 = lists[num]['gradeName']
                sorts1 = lists[num]['sorts']
                new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
                # 要从第二行开始写，所以这里行数要加1
                sheet.write(new_row, 0, gradeName1)
                sheet.write(new_row, 1, sorts1)
            self.xlsc.save(self.gPath)
            print('年级数据写入成功,共', len(lists), '个年级~~')
        else:
            print('该校没有添加年级~')
    # 班级模板部分
    def ClassTemplate(self):
        data = get_Class()
        rows = data['rows']
        lists = []
        if rows:
            for row in rows:
                dic = {}
                name = row['name']
                gradeName = row['gradeName']
                dic['name'] = name
                dic['gradeName'] = gradeName
                lists.append(dic)
            sheet = self.xlsc.get_sheet(3)
            # i既是lis的下标，也代表每一列#处理表头
            for num in range(len(lists)):
                name1 = lists[num]['name']
                gradeName1 = lists[num]['gradeName']
                new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
                # 要从第二行开始写，所以这里行数要加1
                sheet.write(new_row, 0, name1)
                sheet.write(new_row, 1, gradeName1)
                sheet.write(new_row, 2, '2018')
            self.xlsc.save(self.gPath)
            print('班级数据写入成功,共', len(lists), '个班级~~')
        else:
            print('该校没有添加班级~')
    # 学年模板部分
    def SemesterYearTemplate(self):
        data = get_Semester()
        rows = data['rows']
        lists = []
        if rows:
            for row in rows:
                dic = {}
                school_year = row['school_year']
                year = school_year[0:4]
                dic['school_year'] = school_year
                dic['year'] = year
                lists.append(dic)
            sheet = self.xlsc.get_sheet(4)
            # i既是lis的下标，也代表每一列#处理表头
            for num in range(len(lists)):
                school_year1 = lists[num]['school_year']
                year1 = lists[num]['year']
                new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
                # 要从第二行开始写，所以这里行数要加1
                sheet.write(new_row, 0, school_year1)
                sheet.write(new_row, 1, year1)
            self.xlsc.save(self.gPath)
            print('学年数据写入成功,共', len(lists), '个学年~~')
        else:
            print('该校没有添加学年~')
    # 学期模板部分
    def SemesterTemplate(self):
        data = get_Semester()
        rows = data['rows']
        lists = []
        if rows:
            for row in rows:
                dic = {}
                school_year = row['school_year']
                begin_time = row['begin_time']
                begin_time = begin_time.replace("-", "/")
                end_time = row['end_time']
                end_time = end_time.replace("-", "/")
                semester = row['semester']
                Stype = semester[-3:]
                status = row['status']
                dic['school_year'] = school_year
                dic['begin_time'] = begin_time
                dic['end_time'] = end_time
                dic['Stype'] = Stype
                dic['status'] = status
                lists.append(dic)
            sheet = self.xlsc.get_sheet(5)
            # i既是lis的下标，也代表每一列#处理表头
            for num in range(len(lists)):
                school_year1 = lists[num]['school_year']
                begin_time1 = lists[num]['begin_time']
                end_time1 = lists[num]['end_time']
                Stype1 = lists[num]['Stype']
                if lists[num]['status'] == '1':
                    status1 = '当前学期'
                else:
                    status1 = '禁用'
                new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
                # 要从第二行开始写，所以这里行数要加1
                sheet.write(new_row, 0, school_year1)
                sheet.write(new_row, 1, begin_time1)
                sheet.write(new_row, 2, end_time1)
                sheet.write(new_row, 3, Stype1)
                sheet.write(new_row, 4, status1)
            self.xlsc.save(self.gPath)
            print('学期数据写入成功,共', len(lists), '个学期~~')
        else:
            print('该校没有添加学期~')
    # 作息时间模板部分
    def SectionTemplate(self):
        data = get_Section()
        rows = data['rows']
        lists = []
        if rows:
            for row in rows:
                dic = {}
                no = row['no']
                name = row['name']
                periodTimeName = row['periodTimeName']
                startTime = row['startTime']
                startTime = startTime[0:5]
                endTime = row['endTime']
                endTime = endTime[0:5]
                dic['no'] = no
                dic['name'] = name
                dic['periodTimeName'] = periodTimeName
                dic['startTime'] = startTime
                dic['endTime'] = endTime
                lists.append(dic)
            sheet = self.xlsc.get_sheet(6)
            # i既是lis的下标，也代表每一列#处理表头
            for num in range(len(lists)):
                no1 = lists[num]['no']
                name1 = lists[num]['name']
                periodTimeName1 = lists[num]['periodTimeName']
                startTime1 = lists[num]['startTime']
                endTime1 = lists[num]['endTime']
                new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
                # 要从第二行开始写，所以这里行数要加1
                sheet.write(new_row, 0, no1)
                sheet.write(new_row, 1, name1)
                sheet.write(new_row, 2, periodTimeName1)
                sheet.write(new_row, 3, startTime1)
                sheet.write(new_row, 4, endTime1)
            self.xlsc.save(self.gPath)
            print('作息时间数据写入成功,一天共', len(lists), '个节次~~')
        else:
            print('该校没有添加作息时间~')
    # 家长模板部分，该信息为模拟生成
    def ParentTemplate(self):
        i = 200
        sheet = self.xlsc.get_sheet(7)
        # i既是lis的下标，也代表每一列#处理表头
        for num in range(i):
            new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
            # 要从第二行开始写，所以这里行数要加1
            name = Rname()
            sheet.write(new_row, 0, name)
            sheet.write(new_row, 1, '%s%s' % (phoneNum[randint(0, len(phoneNum) - 1)], randint(100000000, 999999999)))
            sheet.write(new_row, 2, Occupation[randint(0, len(Occupation) - 1)])
            sheet.write(new_row, 3, '%s%s区%s栋%s楼%s号' % (
            Nplace[randint(0, len(Nplace) - 1)], GBK2312(randint(2, 4)), randint(1, 30), randint(1, 33),
            randint(1000, 9999)))
            if new_row % 2 == 0:
                sheet.write(new_row, 4, '女')
            else:
                sheet.write(new_row, 4, '男')
            Birthday = '%s/%s/%s' % (randint(1970, 1990), randint(1, 12), randint(1, 31))
            sheet.write(new_row, 5, Birthday)
            sheet.write(new_row, 6, Country[randint(0, len(Country) - 1)])
            sheet.write(new_row, 7, Nation[randint(0, len(Nation) - 1)])
            sheet.write(new_row, 8, Poutlook[randint(0, len(Poutlook) - 1)])
            sheet.write(new_row, 9, '%s%s区%s路%s号' % (
            Nplace[randint(0, len(Nplace) - 1)], GBK2312(randint(2, 4)), GBK2312(randint(2, 4)), randint(100, 999)))
            sheet.write(new_row, 10, '%s@qq.com' % randint(100000000, 999999999))
        self.xlsc.save(self.gPath)
        print('家长数据模拟写入成功,共', i, '个家长~~')
    # 建筑模板部分
    def BuildingTemplate(self):
        data = get_Building()
        rows = data['rows']
        lists = []
        if rows:
            for row in rows:
                dic = {}
                buildingName = row['buildingName']
                dic['buildingName'] = buildingName
                lists.append(dic)
            sheet = self.xlsc.get_sheet(8)
            # i既是lis的下标，也代表每一列#处理表头
            for num in range(len(lists)):
                buildingName1 = lists[num]['buildingName']
                new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
                # 要从第二行开始写，所以这里行数要加1
                sheet.write(new_row, 0, buildingName1)
                sheet.write(new_row, 1, '教学楼')
            self.xlsc.save(self.gPath)
            print('建筑数据写入成功,共', len(lists), '栋建筑~~')
        else:
            print('该校没有添加建筑~')
    # 教室模板部分
    def ClassroomTemplate(self):
        data = get_Classroom()
        rows = data['rows']
        lists = []
        if rows:
            for row in rows:
                dic = {}
                classroomName = row['classroomName']
                buildingName = row['buildingName']
                capacity = row['capacity']
                dic['classroomName'] = classroomName
                dic['buildingName'] = buildingName
                dic['capacity'] = capacity
                lists.append(dic)
            sheet = self.xlsc.get_sheet(9)
            # i既是lis的下标，也代表每一列#处理表头
            for num in range(len(lists)):
                classroomName1 = lists[num]['classroomName']
                buildingName1 = lists[num]['buildingName']
                capacity1 = lists[num]['capacity']
                new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
                # 要从第二行开始写，所以这里行数要加1
                sheet.write(new_row, 0, classroomName1)
                sheet.write(new_row, 1, buildingName1)
                sheet.write(new_row, 3, '普通教室')
                sheet.write(new_row, 4, capacity1)
            self.xlsc.save(self.gPath)
            print('教室数据写入成功,共', len(lists), '间教室~~')
        else:
            print('该校没有添加教室~')
if __name__ == '__main__':
    o = OnekeyInit()
    o.StudentTemplate()
    o.TeacherTemplate()
    o.GradeTemplate()
    o.ClassTemplate()
    o.SemesterYearTemplate()
    o.SemesterTemplate()
    o.SectionTemplate()
    o.ParentTemplate()
    o.BuildingTemplate()
    o.ClassroomTemplate()