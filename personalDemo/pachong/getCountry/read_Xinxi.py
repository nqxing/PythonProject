import os
import random
import logging.handlers
# 从31个省中随机抽取一个省地区信息返回，精确到村，没村信息到镇，以此类推
def read_One():
    dirPath = 'D:\\PythonProject\\PersonalDemo\\pachong\\getCountry\\全国信息\\'
    dirsList = []
    for dName in os.listdir(dirPath):
        name = dName.split('.')[0]
        dirsList.append(name)
    shengName = dirsList[random.randint(0,len(dirsList)-1)]
    f = open("{}{}.txt".format(dirPath,shengName), "r",encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    shengDic = eval(lines[0])[shengName]
    if type(shengDic).__name__ == 'dict':
        shiNameList = list(shengDic.keys())
        shiName = shiNameList[random.randint(0,len(shiNameList)-1)]
        if type(shengDic[shiName]).__name__ == 'dict':
            quNameList = list(shengDic[shiName].keys())
            if quNameList:
                quName = quNameList[random.randint(0,len(quNameList)-1)]
                if type(shengDic[shiName][quName]).__name__ == 'dict':
                    zhenNameList = list(shengDic[shiName][quName].keys())
                    if zhenNameList:
                        zhenName = zhenNameList[random.randint(0, len(zhenNameList) - 1)]
                        cunNameList = shengDic[shiName][quName][zhenName]
                        if cunNameList:
                            cunName = cunNameList[random.randint(0,len(cunNameList)-1)]
                            allName = shengName + shiName + quName + zhenName + cunName
                            return allName
                        else:
                            allName = shengName + shiName + quName + zhenName
                            print(allName,',这个镇没有村信息....')
                            return allName
                    else:
                        allName  = shengName + shiName + quName
                        print(allName,',这个区/县没有镇信息....')
                        return allName

                else:
                    cunNameList = shengDic[shiName][quName]
                    if cunNameList:
                        cunName = cunNameList[random.randint(0, len(cunNameList) - 1)]
                        allName = shengName + shiName + quName + cunName
                        return allName
                    else:
                        allName = shengName + shiName + quName
                        print(allName,',这个镇没有村信息....')
                        return allName
            else:
                allName = shengName + shiName
                print(allName, ',这个市没有区/县信息....')
                return allName


# 指定数量，把全国信息txt文件读取转换成一个字典再从中随机抽取num个省地区信息返回，精确到村，没村信息到镇，以此类推
def read_Num(num):
    # initLogging('D:\\framework_demo\\pachong\\getCountry\\log\\logData.log')
    LOG_FILE = 'D:\\PythonProject\\PersonalDemo\\pachong\\getCountry\\log\\logData.log'
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 实例化handler
    fmt = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter
    logger = logging.getLogger('tst')  # 获取名为tst的logger
    logger.addHandler(handler)  # 为logger添加handler
    logger.setLevel(logging.DEBUG)
    dirPath = 'D:\\PythonProject\\PersonalDemo\\pachong\\getCountry\\全国地区信息'
    f = open("{}.txt".format(dirPath), "r", encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    countryDic = eval(lines[0])
    dirsList = list(countryDic.keys())
    allNameList = [] # 返回地区信息，精确到村
    nPlaceList = [] # 返回籍贯信息，精确到省市
    for n in range(num):
        shengName = dirsList[random.randint(0,len(dirsList)-1)]
        shengDic = countryDic[shengName]
        if type(shengDic).__name__ == 'dict':
            shiNameList = list(shengDic.keys())
            shiName = shiNameList[random.randint(0,len(shiNameList)-1)]
            # 生成籍贯
            nPlaceList.append(shengName+shiName)
            if type(shengDic[shiName]).__name__ == 'dict':
                quNameList = list(shengDic[shiName].keys())
                if quNameList:
                    quName = quNameList[random.randint(0,len(quNameList)-1)]
                    if type(shengDic[shiName][quName]).__name__ == 'dict':
                        zhenNameList = list(shengDic[shiName][quName].keys())
                        if zhenNameList:
                            zhenName = zhenNameList[random.randint(0, len(zhenNameList) - 1)]
                            cunNameList = shengDic[shiName][quName][zhenName]
                            if cunNameList:
                                cunName = cunNameList[random.randint(0,len(cunNameList)-1)]
                                allName = shengName + shiName + quName + zhenName + cunName
                                allNameList.append(allName)
                            else:
                                allName = shengName + shiName + quName + zhenName
                                logger.info('%s,这个镇没有村信息....'%allName)
                                allNameList.append(allName)
                        else:
                            allName  = shengName + shiName + quName
                            logger.info('%s,这个区/县没有镇信息....'%allName)
                            allNameList.append(allName)

                    else:
                        cunNameList = shengDic[shiName][quName]
                        if cunNameList:
                            cunName = cunNameList[random.randint(0, len(cunNameList) - 1)]
                            allName = shengName + shiName + quName + cunName
                            allNameList.append(allName)
                        else:
                            allName = shengName + shiName + quName
                            logger.info('%s,这个镇没有村信息....'%allName)
                            allNameList.append(allName)
                else:
                    allName = shengName + shiName
                    logger.info('%s,这个市没有区/县信息....'%allName)
                    allNameList.append(allName)
    return allNameList,nPlaceList

# 指定数量，先把31个省集中合并成一个字典再从中随机抽取num个省地区信息返回，精确到村，没村信息到镇，以此类推
def read_Num1(num):
    # initLogging('D:\\framework_demo\\pachong\\getCountry\\log\\logData.log')
    LOG_FILE = 'D:\\PythonProject\\PersonalDemo\\pachong\\getCountry\\log\\logData.log'
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 实例化handler
    fmt = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)  # 实例化formatter
    handler.setFormatter(formatter)  # 为handler添加formatter
    logger = logging.getLogger('tst')  # 获取名为tst的logger
    logger.addHandler(handler)  # 为logger添加handler
    logger.setLevel(logging.DEBUG)

    dirPath = 'D:\\PythonProject\\PersonalDemo\\pachong\\getCountry\\全国信息\\'
    dirsList = []
    countryDic = {}
    for dName in os.listdir(dirPath):
        name = dName.split('.')[0]
        dirsList.append(name)
    for i in range(len(dirsList)):
        f = open("{}{}.txt".format(dirPath, dirsList[i]), "r", encoding='utf-8')
        lines = f.readlines()  # 读取全部内容
        shengDic = eval(lines[0])[dirsList[i]]
        countryDic[dirsList[i]] = shengDic
    allNameList = [] # 返回地区信息，精确到村
    nPlaceList = [] # 返回籍贯信息，精确到省市
    for n in range(num):
        shengName = dirsList[random.randint(0,len(dirsList)-1)]
        shengDic = countryDic[shengName]
        if type(shengDic).__name__ == 'dict':
            shiNameList = list(shengDic.keys())
            shiName = shiNameList[random.randint(0,len(shiNameList)-1)]
            # 生成籍贯
            nPlaceList.append(shengName+shiName)
            if type(shengDic[shiName]).__name__ == 'dict':
                quNameList = list(shengDic[shiName].keys())
                if quNameList:
                    quName = quNameList[random.randint(0,len(quNameList)-1)]
                    if type(shengDic[shiName][quName]).__name__ == 'dict':
                        zhenNameList = list(shengDic[shiName][quName].keys())
                        if zhenNameList:
                            zhenName = zhenNameList[random.randint(0, len(zhenNameList) - 1)]
                            cunNameList = shengDic[shiName][quName][zhenName]
                            if cunNameList:
                                cunName = cunNameList[random.randint(0,len(cunNameList)-1)]
                                allName = shengName + shiName + quName + zhenName + cunName
                                allNameList.append(allName)
                            else:
                                allName = shengName + shiName + quName + zhenName
                                logger.info('%s,这个镇没有村信息....'%allName)
                                allNameList.append(allName)
                        else:
                            allName  = shengName + shiName + quName
                            logger.info('%s,这个区/县没有镇信息....'%allName)
                            allNameList.append(allName)

                    else:
                        cunNameList = shengDic[shiName][quName]
                        if cunNameList:
                            cunName = cunNameList[random.randint(0, len(cunNameList) - 1)]
                            allName = shengName + shiName + quName + cunName
                            allNameList.append(allName)
                        else:
                            allName = shengName + shiName + quName
                            logger.info('%s,这个镇没有村信息....'%allName)
                            allNameList.append(allName)
                else:
                    allName = shengName + shiName
                    logger.info('%s,这个市没有区/县信息....'%allName)
                    allNameList.append(allName)
    return allNameList,nPlaceList