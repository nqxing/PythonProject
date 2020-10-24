aqh_headers = {
'Host':	'weixin.chinaredstar.com',
'Upgrade-Insecure-Requests':	'1',
'User-Agent':	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
'Accept':	'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# 'Referer':	'http://weixin.chinaredstar.com/ticket/poster_index.html?userkey=c59bbb7c73c14918a61c6e0c8191ff53&poster_id=10367&from_openid=opkpxt1R4G671WyBsczEqZ5tteUk&poster_channel=26079&poster_from=&parentCode=SRGf6bMYbRiRUQ/MPVr5vbvC4jrktkoIitio3Re9hb73uUJIj4C%20UnFOb//fauIejD6Vvyo/3FVzw2Y4KI4ds0x2iYqgW/neS%20cquaUDGAOvqQD8etU0/ZdAxx98ZJ%20hYcjF4CX2LCzT/SXIEK3%20y4xypn6K3cNfa7DsJfX%20drw=',
'Accept-Encoding':	'gzip, deflate',
'Accept-Language':	'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
'Cookie':	'ASP.NET_SessionId=2s2rlunidqyr5qjenng5kpvv; 8gsamxz5=1589340366699',
'Connection':	'keep-alive'
}

# aqh_url = 'http://weixin.chinaredstar.com/ticket/poster_index.html?userkey=8a72238128d446878c97c2130b10cfa3&poster_id=10367&from_openid=opkpxt1R4G671WyBsczEqZ5tteUk&poster_channel=26079&poster_from=&parentCode=SRGf6bMYbRiRUQ/MPVr5vbvC4jrktkoIitio3Re9hb73uUJIj4C%20UnFOb//fauIejD6Vvyo/3FVzw2Y4KI4ds0x2iYqgW/neS%20cquaUDGAOvqQD8etU0/ZdAxx98ZJ%20hYcjF4CX2LCzT/SXIEK3%20y4xypn6K3cNfa7DsJfX%20drw='
aqh_url = 'http://weixin.chinaredstar.com/ticket/poster_mid.aspx?poster_id=10367&from_openid=opkpxt1R4G671WyBsczEqZ5tteUk&poster_channel=26079&parentCode=SRGf6bMYbRiRUQ/MPVr5vbvC4jrktkoIitio3Re9hb73uUJIj4C+UnFOb//fauIejD6Vvyo/3FVzw2Y4KI4ds0x2iYqgW/neS+cquaUDGAOvqQD8etU0/ZdAxx98ZJ+hYcjF4CX2LCzT/SXIEK3+y4xypn6K3cNfa7DsJfX+drw='

# r = requests.get(aqh_url)
# print(r.text)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import re
import traceback
from bs4 import BeautifulSoup
class getIp:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
    def Join_ip(self,urls):
        for u in range(len(urls)):
            r = requests.get(urls[u],headers=self.headers,verify=False).text
            soup = BeautifulSoup(r, 'lxml')
            # print(soup)
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
                # r = requests.get(aqh_url, headers=aqh_headers, proxies=proxies, timeout=15)
                # print(aqh_url)
                # print(i, r.text)
                r = test1(proxies)
                # if "车建新：把疫情的损失10倍夺回来" in r:
                if '"code":200' in r:
                    print('测试进度-({}/{}),{},有效ip~~'.format(i+1,len(ips),ips[i]))
                else:
                    pass
                    # print('测试进度-({}/{}),{},未知错误~~{}'.format(i+1,len(ips),ips[i],r.status_code))
            except Exception as e:
                pass
                # print(traceback.format_exc())
    def main(self):
        urls = []
        for i in range(1,20):
            url = 'https://www.xicidaili.com/nt/'+ str(i)
            # url = 'http://www.xicidaili.com/wt/' + str(i)
            urls.append(url)
        self.Join_ip(urls)


def test1(proxies):
    import requests

    headers = {
        'Host': 'aureuma.mmall.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
        'Accept': 'image/webp,image/*,*/*;q=0.8',
        'Referer': 'http://weixin.chinaredstar.com/ticket/poster_index.html?userkey=c39e99b9984c42c6a6d2b3be27952dbf&poster_id=10367&from_openid=opkpxt1R4G671WyBsczEqZ5tteUk&poster_channel=26079&poster_from=&parentCode=SRGf6bMYbRiRUQ/MPVr5vbvC4jrktkoIitio3Re9hb73uUJIj4C%20UnFOb//fauIejD6Vvyo/3FVzw2Y4KI4ds0x2iYqgW/neS%20cquaUDGAOvqQD8etU0/ZdAxx98ZJ%20hYcjF4CX2LCzT/SXIEK3%20y4xypn6K3cNfa7DsJfX%20drw=',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
    }

    params = (
        ('ts', '1589352278542'),
        ('page', ''),
        ('service', 'wx'),
        ('version', '1.0'),
        ('p_domain', ''),
        ('p_channel', ''),
        ('p_type', ''),
        ('p_id', '8f86cd78dae07bce795f303892a1134e'),
        ('p_url',
         'http://weixin.chinaredstar.com/ticket/poster_index.html?userkey=c39e99b9984c42c6a6d2b3be27952dbf&poster_id=10367&from_openid=opkpxt1R4G671WyBsczEqZ5tteUk&poster_channel=26079&poster_from=&parentCode=SRGf6bMYbRiRUQ/MPVr5vbvC4jrktkoIitio3Re9hb73uUJIj4C%20UnFOb//fauIejD6Vvyo/3FVzw2Y4KI4ds0x2iYqgW/neS%20cquaUDGAOvqQD8etU0/ZdAxx98ZJ%20hYcjF4CX2LCzT/SXIEK3%20y4xypn6K3cNfa7DsJfX%20drw='),
        ('app_v', ''),
        ('app_b', ''),
        ('d_prixel_x', '687'),
        ('d_prixel_y', '636'),
        ('u_mid', 'opkpxt-9825XcnW6jztT2aRo3fak'),
        ('id', '8428'),
        ('u_city', ''),
        ('u_idfa', ''),
        ('p_title', ''),
        ('p_v1', 'unionid=&scene=&source_from=1&mall_code=&ticketid=&poster_id=10367&marketingall'),
        ('p_v2', 'nickname= &sex=&headimgurl='),
        ('p_v3', 'marketingall'),
        ('d_os', 'Windows7'),
        ('d_os_version', ''),
        ('d_mark', ''),
        ('d_model', ''),
        ('d_browser',
         '{"appName":"Netscape","appVersion":"5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat","enable":-1,"userAgent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat","language":"zh-CN","cookieEnabled":1}'),
        ('u_id', 'c622fe9395614300b3c40ca5013eae3b'),
        ('u_guid', '1589352278542--'),
        ('u_phone', ''),
        ('l_country', ''),
        ('l_province', ''),
        ('l_city', ''),
        ('l_dist', ''),
        ('l_ip', ''),
        ('l_gps', ''),
        ('r_keyword', ''),
        ('r_url', ''),
        ('r_from', ''),
    )

    response = requests.get('http://aureuma.mmall.com/p', headers=headers, params=params,proxies=proxies)

    print(response.text)
    return response.text

if __name__ == '__main__':
    c = getIp()
    c.main()
# test1()

