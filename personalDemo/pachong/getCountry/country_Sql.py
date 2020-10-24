import pymysql
def savaSql():
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='nqxing')
    cursor = db.cursor()
    sql = 'INSERT INTO country(id, name, pid, type) VALUES(%s, %s, %s, %s) '
    id = 0
    # dirPath = 'D:\\framework_demo\\pachong\\getCountry\\'
    dirPath = 'D:\\PythonProject\\PersonalDemo\\pachong\\getCountry\\全国信息\\'
    f = open("{}海南省.txt".format(dirPath), "r",encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    shengDic = eval(lines[0])
    shengNameList = list(shengDic.keys())
    shiPidDic = {}
    for i in range(len(shengNameList)):
        id+=1
        name = shengNameList[i]
        pid = 0
        try:
            cursor.execute(sql, (id, name, pid, '1'))
            db.commit()
            # 获取该省下的所有市名组成一个列表
            t_shiList = list(shengDic[name].keys())
            # 把市名（列表）和该省的id组成一个新字典，该字典的键（也就是该省id）就是后面市名的pid
            shiPidDic[id] = t_shiList
            print(id)
        except:
            db.rollback()
            db.close()
    # 把上面市新字典的键（省的id）组成一个列表
    shiIdList = list(shiPidDic.keys())
    quPidDic = {}
    for shiId in shiIdList:
        # sql查询语句查询省id得出省名
        cx_sql = 'SELECT * FROM country WHERE id = %d' % shiId
        cursor.execute(cx_sql)
        oneSheng = cursor.fetchone()
        # 市新字典访问省id得出该省下的所有市名
        shiNameList = shiPidDic[shiId]
        for shiName in shiNameList:
            id += 1
            try:
                cursor.execute(sql, (id, shiName, shiId ,'2'))
                db.commit()
                # 通过访问省名+市名得到该市下的所有区/县名，组成一个列表
                t_quList = list(shengDic[oneSheng[1]][shiName].keys())
                # 把县名（列表）和该市的id组成一个新字典，该字典的键（也就是该市id）就是后面区/县名的pid
                quPidDic[id] = t_quList
                print(id)
            except:
                db.rollback()
                db.close()
    # 把上面区/县新字典的键（市的id）组成一个列表
    quIdList = list(quPidDic.keys())
    zhenPidDic = {}
    pZhenPidDic = {}
    for quId in quIdList:
        # sql查询语句查询市id得出市名，再根据市名查询出该市pid，再根据市id得出省名
        cx_sql = 'SELECT * FROM country WHERE id = %d' % quId
        cursor.execute(cx_sql)
        oneShi = cursor.fetchone()[1]
        cx_sql = 'SELECT * FROM country WHERE name = "%s"' % oneShi
        cursor.execute(cx_sql)
        cx_sql = 'SELECT * FROM country WHERE id = %d' % cursor.fetchone()[2]
        cursor.execute(cx_sql)
        oneSheng = cursor.fetchone()[1]
        # 区/县新字典访问市id得出该市下的所有区县名
        quNameList = quPidDic[quId]
        for quName in quNameList:
            id += 1
            try:
                cursor.execute(sql, (id, quName, quId ,'3'))
                db.commit()
                # 判断访问的类型是否为字典，再通过访问省名+市名+区/县名得到该区/县下的所有镇名，组成一个列表
                if type(shengDic[oneSheng][oneShi][quName]).__name__ == 'dict':
                    t_zhenList = list(shengDic[oneSheng][oneShi][quName].keys())
                    # 把镇名（列表）和该区/县的id组成一个新字典，该字典的键（也就是该区/县id）就是后面镇名的pid
                    zhenPidDic[id] = t_zhenList
                # 判断访问的类型是否为列表，如果是列表则该市下没有区县，直接访问省名+市名+镇名，列表组成一个字典，该字典的键（也就是该镇id）就是后面村名的pid
                elif type(shengDic[oneSheng][oneShi][quName]).__name__ == 'list':
                    pZhenPidDic[id] = shengDic[oneSheng][oneShi][quName]
                print(id)
            except:
                db.rollback()
                db.close()

    # 把上面镇新字典的键（区/县的id）组成一个列表
    zhenIdList = list(zhenPidDic.keys())
    cunPidDic = {}
    for zhenId in zhenIdList:
        # sql查询语句查询区/县id得去区/县名，再根据区/县的pid（市id）查询出该市，再根据市名查出市的pid，再得出省名
        cx_sql = 'SELECT * FROM country WHERE id = %d' % zhenId
        cursor.execute(cx_sql)
        tDic = cursor.fetchone()
        oneQu = tDic[1]
        tid = int(tDic[2])
        cx_sql = 'SELECT * FROM country WHERE id = %d' % tid
        cursor.execute(cx_sql)
        oneShi = cursor.fetchone()[1]
        cx_sql = 'SELECT * FROM country WHERE name = "%s"' % oneShi
        cursor.execute(cx_sql)
        cx_sql = 'SELECT * FROM country WHERE id = %d' % cursor.fetchone()[2]
        cursor.execute(cx_sql)
        oneSheng = cursor.fetchone()[1]
        # 镇新字典访问区县id得出该区县下的所有镇名
        zhenNameList = zhenPidDic[zhenId]
        for zhenName in zhenNameList:
            id += 1
            try:
                cursor.execute(sql, (id, zhenName, zhenId ,'4'))
                db.commit()
                cunPidDic[id] = shengDic[oneSheng][oneShi][oneQu][zhenName]
                print(id)
            except:
                db.rollback()
                db.close()

    pZhenIdList = list(pZhenPidDic.keys())
    for pZhenId in pZhenIdList:
        pZhenNameList = pZhenPidDic[pZhenId]
        for pZhenName in pZhenNameList:
            id += 1
            try:
                cursor.execute(sql, (id, pZhenName, pZhenId ,'5'))
                db.commit()
                print('p---{}'.format(id))
            except:
                db.rollback()
                db.close()

    cunIdList = list(cunPidDic.keys())
    for cunId in cunIdList:
        cunNameList = cunPidDic[cunId]
        for cunName in cunNameList:
            id += 1
            try:
                cursor.execute(sql, (id, cunName, cunId ,'5'))
                db.commit()
                print(id)
            except:
                db.rollback()
                db.close()
savaSql()