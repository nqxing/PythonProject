import requests
from bs4 import BeautifulSoup
import threadpool
import os
import time
uUrl = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/'
# 获取文件夹下的所有文件名并加入到新的数组（不含文件后缀）
def get_Dir():
    dirsList = []
    for dName in os.listdir('txt\\'):
        name = dName.split('.')[0]
        dirsList.append(name)
    return dirsList
def get_Sheng():
    dirsList = get_Dir()
    url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html'
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        'Accept-Encoding': ''
    }
    html = requests.get(url, headers=headers)
    html.encoding = 'GBK'
    html = html.text
    soup = BeautifulSoup(html, 'lxml')
    shengUrlList = []
    shengNameList = []
    trList = soup.find_all(class_='provincetr')
    for tr in trList:
        tdList = tr.find_all(name='td')
        for td in tdList:
            aList = td.find_all(name='a')
            for a in aList:
                # 获取所有省链接
                shengUrlList.append('%s%s'%(uUrl,a['href']))
                # 获取所有省名字
                shengNameList.append(a.get_text())
    # 把txt文件夹下的已下载的省进行移除，不加入待获取的省列表
    for dirName in dirsList:
        index = shengNameList.index(dirName)
        del shengNameList[int(index)]
        del shengUrlList[int(index)]
    # 如果省名和省链接数组都不为空就一直执行，直到爬取完毕
    while shengNameList and shengUrlList:
        # 数组大于2个时就以2为单位加入多线程（实测一次跑两个省为最佳，不会被服务器检测）
        if len(shengNameList) >= 2:
            newShengNameList = []
            newShengUrlList = []
            newShengNameList.append(shengNameList[0])
            newShengNameList.append(shengNameList[1])
            newShengUrlList.append(shengUrlList[0])
            newShengUrlList.append(shengUrlList[1])
            data = [((newShengUrlList, newShengNameList), None) for (newShengUrlList, newShengNameList) in
                    zip(newShengUrlList, newShengNameList)]  # (index,i)也可以写成[index,i]
            pool = threadpool.ThreadPool(2)
            requests1 = threadpool.makeRequests(get_Shi, data)
            [pool.putRequest(req) for req in requests1]
            pool.wait()
            del shengNameList[0]
            del shengUrlList[0]
            del shengNameList[0]
            del shengUrlList[0]
        else:
            newShengNameList = []
            newShengUrlList = []
            newShengNameList.append(shengNameList[0])
            newShengUrlList.append(shengUrlList[0])
            data = [((newShengUrlList, newShengNameList), None) for (newShengUrlList, newShengNameList) in
                    zip(newShengUrlList, newShengNameList)]  # (index,i)也可以写成[index,i]
            pool = threadpool.ThreadPool(1)
            requests1 = threadpool.makeRequests(get_Shi, data)
            [pool.putRequest(req) for req in requests1]
            pool.wait()
            del shengNameList[0]
            del shengUrlList[0]
        time.sleep(10)
        print('--------------')
    print('任务已结束~~')
def get_Shi(shengUrl,shengName):
    print('正在爬取{}信息...'.format(shengName))
    shengDic = {}
    sList = [] # 市以下列表变量，值为包含区县、镇、村信息的字典
    shiUrlList = []
    shiNameList = []
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    html = requests.get(shengUrl, headers=headers)
    html.encoding = 'GBK'
    html = html.text
    soup = BeautifulSoup(html, 'lxml')
    trList = soup.find_all(class_='citytr')
    # 判断是否为市辖区城市，如北京市，天津市。trList列表长度若为1，页面就是 110100000000	市辖区，判定为市辖区城市
    trNum = len(trList)
    if trNum<=2:
        for tr in trList:
            aList = tr.find_all(name='a')
            ourl = '%s%s' % (uUrl, aList[-1]['href'])
            # purl 主要为url前缀，获取a:href属性值后+purl前缀，拼接为下级url访问链接
            purl  = aList[-1]['href'][0:3] # 此处截取链接前3位，如11/1101.html，截取后为11/
            ohtml = requests.get(ourl, headers=headers)
            ohtml.encoding = 'GBK'
            ohtml = ohtml.text
            soup = BeautifulSoup(ohtml, 'lxml')
            trList = soup.find_all(class_='countytr')
            for tr in trList:
                tdList = tr.find_all(name='td')
                for i in range(int(len(tdList)/2)):
                    j = i*2
                    del tdList[j]
                for td in tdList:
                    aList = td.find_all(name='a')
                    for a in aList:
                        shiUrlList.append('%s%s%s' % (uUrl, purl, a['href']))
                        shiNameList.append(a.get_text())
        # 新建一个市辖区级空字典
        tShiDic = {}
        # 将获取到的市辖区名赋值到空市辖区字典中，如：{‘东城区’：‘’}
        for sName in shiNameList:
            tShiDic[sName] = ''
        # 再将市辖区赋值给省级空字典中，如：{‘北京市’：{‘东城区’：‘’}}
        shengDic[shengName] = tShiDic
        # 获取街道
        for num in range(len(shiUrlList)):
            pList = shiUrlList[num].split('/')
            del pList[0]
            del pList[-1]
            pUrl = 'http:/{}/'.format('/'.join(pList))  # 此处通过字符串分隔方式获取purl，然后拼接成下级url访问链接
            # 失败重试次数
            jieNum = 0
            shequNum = 0
            jieUrlList = []
            jieNameList = []
            shequList = []
            html = requests.get(shiUrlList[num], headers=headers)
            html.encoding = 'GBK'
            html = html.text
            soup = BeautifulSoup(html, 'lxml')
            trList = soup.find_all(class_='towntr')
            for tr in trList:
                tdList = tr.find_all(name='td')
                for i in range(int(len(tdList) / 2)):
                    j = i * 2
                    del tdList[j]
                for td in tdList:
                    aList = td.find_all(name='a')
                    for a in aList:
                        jieUrlList.append('%s%s' % (pUrl, a['href']))
                        jieNameList.append(a.get_text())

            while len(jieNameList) == 0 and len(jieUrlList) == 0 and jieNum < 5:
                html = requests.get(shiUrlList[num], headers=headers)
                html.encoding = 'GBK'
                html = html.text
                soup = BeautifulSoup(html, 'lxml')
                trList = soup.find_all(class_='towntr')
                for tr in trList:
                    tdList = tr.find_all(name='td')
                    for i in range(int(len(tdList) / 2)):
                        j = i * 2
                        del tdList[j]
                    for td in tdList:
                        aList = td.find_all(name='a')
                        for a in aList:
                            jieUrlList.append('%s%s' % (pUrl, a['href']))
                            jieNameList.append(a.get_text())
                jieNum+=1

            tJieDic = {}
            for name in jieNameList:
                tJieDic[name] = ''
            # 获取社区居委会

            for num1 in range(len(jieUrlList)):
                shequNameList = []
                html = requests.get(jieUrlList[num1], headers=headers)
                html.encoding = 'GBK'
                html = html.text
                soup = BeautifulSoup(html, 'lxml')
                trList = soup.find_all(class_='villagetr')
                for tr in trList:
                    tdList = tr.find_all(name='td')
                    shequNameList.append(tdList[-1].get_text())

                while len(shequNameList) == 0 and shequNum < 5:
                    html = requests.get(jieUrlList[num1], headers=headers)
                    html.encoding = 'GBK'
                    html = html.text
                    soup = BeautifulSoup(html, 'lxml')
                    trList = soup.find_all(class_='villagetr')
                    for tr in trList:
                        tdList = tr.find_all(name='td')
                        shequNameList.append(tdList[-1].get_text())
                    shequNum+=1

                shequList.append(shequNameList)

            tJieList = list(tJieDic.keys())
            for ti in range(len(tJieList)):
                tJieDic[tJieList[ti]] = shequList[ti]
            sList.append(tJieDic)
    # 否则就是省会城市，如：福建省，广东省
    else:
        # 获取市
        for tr in trList:
            tdList = tr.find_all(name='td')
            for i in range(int(len(tdList)/2)):
                j = i*2
                del tdList[j]
            for td in tdList:
                aList = td.find_all(name='a')
                for a in aList:
                    shiUrlList.append('%s%s' % (uUrl, a['href']))
                    shiNameList.append(a.get_text())
        tShiDic = {}
        for sName in shiNameList:
            tShiDic[sName] = ''
        shengDic[shengName] = tShiDic
        # 获取区县
        pList = shiUrlList[0].split('/')
        del pList[0]
        del pList[-1]
        pUrl = 'http:/{}/'.format('/'.join(pList))
        for num in range(len(shiUrlList)):
            quUrlList = []
            quNameList = []
            html = requests.get(shiUrlList[num], headers=headers)
            html.encoding = 'GBK'
            html = html.text
            soup = BeautifulSoup(html, 'lxml')
            trList = soup.find_all(class_='countytr')
            for tr in trList:
                tdList = tr.find_all(name='td')
                for i in range(int(len(tdList) / 2)):
                    j = i * 2
                    del tdList[j]
                for td in tdList:
                    aList = td.find_all(name='a')
                    for a in aList:
                        quUrlList.append('%s%s' % (pUrl, a['href']))
                        quNameList.append(a.get_text())
            # 判断区列表是否为空，广东省（东莞市、中山市），海南省（儋州市）下级没有区、县
            if quUrlList:
                tQuDic = {}
                for name in quNameList:
                    tQuDic[name] = ''
                # 获取镇
                zhenList = []
                pList = quUrlList[0].split('/')
                del pList[0]
                del pList[-1]
                pUrl1 = 'http:/{}/'.format('/'.join(pList))
                for num2 in range(len(quUrlList)):
                    zhenNameList = []
                    zhenUrlList = []
                    # 失败重试次数
                    zhenNum = 0
                    cunNum = 0
                    html = requests.get(quUrlList[num2], headers=headers)
                    html.encoding = 'GBK'
                    html = html.text
                    soup = BeautifulSoup(html, 'lxml')
                    trList = soup.find_all(class_='towntr')
                    for tr in trList:
                        tdList = tr.find_all(name='td')
                        for i in range(int(len(tdList) / 2)):
                            j = i * 2
                            del tdList[j]
                        for td in tdList:
                            aList = td.find_all(name='a')
                            for a in aList:
                                zhenUrlList.append('%s%s' % (pUrl1, a['href']))
                                zhenNameList.append(a.get_text())

                    while len(zhenNameList) == 0 and len(zhenUrlList) == 0 and zhenNum < 5:
                        html = requests.get(quUrlList[num2], headers=headers)
                        html.encoding = 'GBK'
                        html = html.text
                        soup = BeautifulSoup(html, 'lxml')
                        trList = soup.find_all(class_='towntr')
                        for tr in trList:
                            tdList = tr.find_all(name='td')
                            for i in range(int(len(tdList) / 2)):
                                j = i * 2
                                del tdList[j]
                            for td in tdList:
                                aList = td.find_all(name='a')
                                for a in aList:
                                    zhenUrlList.append('%s%s' % (pUrl1, a['href']))
                                    zhenNameList.append(a.get_text())
                        zhenNum+=1

                    tZhenDic = {}
                    for zi in range(len(zhenNameList)):
                        tZhenDic[zhenNameList[zi]] = ''
                    # 获取村
                    tCunList = []
                    for num3 in range(len(zhenUrlList)):
                        cunNameList = []
                        html = requests.get(zhenUrlList[num3], headers=headers)
                        html.encoding = 'GBK'
                        html = html.text
                        soup = BeautifulSoup(html, 'lxml')
                        trList = soup.find_all(class_='villagetr')
                        for tr in trList:
                            tdList = tr.find_all(name='td')
                            cunNameList.append(tdList[-1].get_text())

                        while len(cunNameList) == 0 and cunNum < 5:
                            html = requests.get(zhenUrlList[num3], headers=headers)
                            html.encoding = 'GBK'
                            html = html.text
                            soup = BeautifulSoup(html, 'lxml')
                            trList = soup.find_all(class_='villagetr')
                            for tr in trList:
                                tdList = tr.find_all(name='td')
                                cunNameList.append(tdList[-1].get_text())
                            cunNum+=1

                        tCunList.append(cunNameList)

                    tzhenList = list(tZhenDic.keys())
                    for ti in range(len(tzhenList)):
                        tZhenDic[tzhenList[ti]] = tCunList[ti]
                    zhenList.append(tZhenDic)
                tQuList = list(tQuDic.keys())
                for ti in range(len(tQuList)):
                    tQuDic[tQuList[ti]] = zhenList[ti]
                sList.append(tQuDic)
            # 这里的就是没有区县的城市，直接获取镇
            else:
                # 获取镇
                zhenNameList = []
                zhenUrlList = []
                html = requests.get(shiUrlList[num], headers=headers)
                html.encoding = 'GBK'
                html = html.text
                soup = BeautifulSoup(html, 'lxml')
                trList = soup.find_all(class_='towntr')
                for tr in trList:
                    tdList = tr.find_all(name='td')
                    for i in range(int(len(tdList) / 2)):
                        j = i * 2
                        del tdList[j]
                    for td in tdList:
                        aList = td.find_all(name='a')
                        for a in aList:
                            zhenUrlList.append('%s%s' % (pUrl, a['href']))
                            zhenNameList.append(a.get_text())
                tzhenDic = {}
                for name in zhenNameList:
                    tzhenDic[name] = ''
                # 获取村
                tCunList = []
                for num3 in range(len(zhenUrlList)):
                    cunNameList = []
                    cunNum = 0
                    html = requests.get(zhenUrlList[num3], headers=headers)
                    html.encoding = 'GBK'
                    html = html.text
                    soup = BeautifulSoup(html, 'lxml')
                    trList = soup.find_all(class_='villagetr')
                    for tr in trList:
                        tdList = tr.find_all(name='td')
                        cunNameList.append(tdList[-1].get_text())

                    while len(cunNameList) == 0 and cunNum < 5:
                        html = requests.get(zhenUrlList[num3], headers=headers)
                        html.encoding = 'GBK'
                        html = html.text
                        soup = BeautifulSoup(html, 'lxml')
                        trList = soup.find_all(class_='villagetr')
                        for tr in trList:
                            tdList = tr.find_all(name='td')
                            cunNameList.append(tdList[-1].get_text())
                        cunNum+=1

                    tCunList.append(cunNameList)
                tzhenList = list(tzhenDic.keys())
                for ti in range(len(tzhenList)):
                    tzhenDic[tzhenList[ti]] = tCunList[ti]
                sList.append(tzhenDic)
    # 获取市级的字典键值名，组成一个列表
    sAList = list(shengDic[shengName].keys())
    for i in range(len(sAList)):
        # 再将县区村组成的字典赋值给市级字典，覆盖之前的空值
        shengDic[shengName][sAList[i]] = sList[i]
    with open("txt\\{}.txt".format(shengName), "w", encoding='utf-8') as f:
        f.write(str(shengDic))
    print('{}爬取成功~~'.format(shengName))
get_Sheng()