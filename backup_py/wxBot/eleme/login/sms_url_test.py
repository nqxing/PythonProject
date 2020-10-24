from bs4 import BeautifulSoup
# from config.config import *
import requests

proxy = '178.213.13.136:53281'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

html = requests.get('https://www.pdflibr.com/SMSContent/48', headers=HEADERS, proxies=proxies, timeout=20)
if html.status_code == 200:
    Soup = BeautifulSoup(html.content, 'lxml')
    print(Soup)
    trList = Soup.find_all(name='tbody')[0].find_all(name='tr')
    if trList:
        for tr in trList:
            tdContent = tr.find_all(name='td')[2].string
            print(tdContent)
            # if '【饿了么】' in tdContent:
            #     validate_code = re.findall('验证码是(.*?)，', tdContent, re.S)[0]