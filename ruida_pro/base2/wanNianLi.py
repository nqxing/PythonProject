import requests
from bs4 import BeautifulSoup

def get_data():
    monthList = []
    year = 2019
    urlList = []
    uUrl = 'https://wannianli.tianqi.com/{}/'.format(year)
    for y in range(1,13):
        if y<10:
            rUrl = '{}0{}/'.format(uUrl,y)
            urlList.append(rUrl)
        else:
            rUrl = '{}{}/'.format(uUrl,y)
            urlList.append(rUrl)
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    for url in urlList:
        monthDic = {}
        html = requests.get(url,headers=headers)
        soup = BeautifulSoup(html.content, 'lxml')
        ul = soup.find_all(class_='date')
        liList = ul[0].find_all(name='li')
        for li in liList:
            g = li.find_all(class_='g')
            n = li.find_all(class_='n')
            if g and n:
                gStr = g[0].get_text()
                nStr = n[0].get_text()
                monthDic[gStr.strip()] = nStr.strip()
        monthList.append(monthDic)
    return year,monthList
def get_data1():
    yearDic = {}
    week = 2
    year = 2019
    urlList = []
    uUrl = 'https://wannianrili.51240.com/ajax/?q={}-{}&v=18121803'
    for y in range(1,13):
        if y<10:
            rUrl = uUrl.format(year,'0'+str(y))
            urlList.append(rUrl)
        else:
            rUrl = uUrl.format(year,y)
            urlList.append(rUrl)
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    for i in range(0,len(urlList)):
        monthDic = {}
        html = requests.get(urlList[i], headers=headers)
        soup = BeautifulSoup(html.content, 'lxml')
        riqiList = soup.find_all(class_='wnrl_riqi')
        for riqi in riqiList:
            dayList = []
            g = riqi.find_all(class_='wnrl_td_gl')
            n = riqi.find_all(class_='wnrl_td_bzl')
            gStr = g[0].get_text()
            nStr = n[0].get_text()
            if riqi.find_all(class_='wnrl_riqi_xiu'):
                nStr+='(休)'
            dayList.append(week)
            if week == 7:
                week = 0
            week+=1
            dayList.append(gStr)
            dayList.append(nStr)
            monthDic[gStr] = dayList
        yearDic[i+1] = monthDic
    return yearDic