def tea_xiaoxue_Class(classNum):
    tea_gradeList = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级']
    tea_classNameList = []
    for g in range(len(tea_gradeList)):
        for i in range(classNum):
            tea_classNameList.append('{}-{}班'.format(tea_gradeList[g], i + 1))
    return tea_gradeList,tea_classNameList

def tea_chuzhong_Class(classNum):
    tea_classNameList = []
    tea_gradeList = ['初一', '初二', '初三']
    for g in range(len(tea_gradeList)):
        for i in range(classNum):
            tea_classNameList.append('{}-{}班'.format(tea_gradeList[g], i + 1))
    return tea_gradeList,tea_classNameList

def tea_gaozhong_Class(classNum):
    tea_classNameList = []
    tea_gradeList = ['高一', '高二', '高三']
    for g in range(len(tea_gradeList)):
        for i in range(classNum):
            tea_classNameList.append('{}-{}班'.format(tea_gradeList[g], i + 1))
    return tea_gradeList,tea_classNameList

def tea_wanzhong_Class(classNum):
    tea_classNameList = []
    tea_gradeList = ['高一', '高二', '高三', '初一', '初二', '初三']
    for g in range(len(tea_gradeList)):
        for i in range(classNum):
            tea_classNameList.append('{}-{}班'.format(tea_gradeList[g], i + 1))
    return tea_gradeList,tea_classNameList

def tea_jiunianzhi_Class(classNum):
    tea_gradeList = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级', '七年级', '八年级', '九年级']
    tea_classNameList = []
    for g in range(len(tea_gradeList)):
        for i in range(classNum):
            tea_classNameList.append('{}-{}班'.format(tea_gradeList[g], i + 1))
    return tea_gradeList,tea_classNameList
# tea_xiaoxue_Class(1)
# tea_chuzhong_Class(1)
# tea_gaozhong_Class(1)
# tea_wanzhong_Class(1)
# tea_jiunianzhi_Class(1)