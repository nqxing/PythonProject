import requests
import re
from bs4 import BeautifulSoup
class getIp:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
    def Join_ip(self,urls):
        for u in range(len(urls)):
            r = requests.get(urls[u],headers=self.headers).text
            soup = BeautifulSoup(r, 'lxml')
            # print(soup.select('#ip_list'))
            table = soup.find(id='ip_list')
            trList = table.find_all(name='tr')
            del trList[0]
            ips = []
            for i in range(len(trList)):
                ip = trList[i].select('td')[1].string +':'+ trList[i].select('td')[2].string
                ips.append(ip)
            self.val_ip(ips)
    def val_ip(self,ips):
        for i in range(len(ips)):
            proxy = ips[i]
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
            try:
                # r = requests.get('http://httpbin.org/get', proxies=proxies, timeout=10)
                # r = requests.get('https://h5.ele.me/restapi/marketing/themes/3971/group_sns/2a3c4d71132f9c27', proxies=proxies, timeout=15)
                # r = requests.get('https://www.pdflibr.com/SMSContent/48',
                #                  proxies=proxies, timeout=15)
                r = requests.get('https://h5.ele.me/restapi/eus/login/mobile_send_code', proxies=proxies, timeout=15)
                print(r.text)
                if "请稍后重试" in r.text:
                    print('测试进度-({}/{}),{},有效ip~~'.format(i+1,len(ips),ips[i]))
                else:
                    print('测试进度-({}/{}),{},未知错误~~{}'.format(i+1,len(ips),ips[i],r.status_code))
            except Exception as e:
                pass
    def main(self):
        urls = []
        for i in range(1,10):
            url = 'http://www.xicidaili.com/wt/' + str(i)
            urls.append(url)
        self.Join_ip(urls)
if __name__ == '__main__':
    c = getIp()
    c.main()