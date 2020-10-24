import requests
from pyquery import PyQuery as pq
import time
url = 'https://ssl.mall.cmbchina.com/_CL5_/Product/Detail?productCode=S1H-700-2XM_019&pushwebview=1&productIndex=9'
headers = {
'Host': 'ssl.mall.cmbchina.com',
'Connection': 'keep-alive',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; huawei nxt-al10 Build/LMY48Z) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Safari/537.36;(cmblife 7.3.0/92 v2)',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,en-US;q=0.8',
'Cookie': 'sajssdk_2015_cross_new_user=1; pgv_pvi=852528128; pgv_si=s337590272; searchHistoryCookie=%5B%7B%22name%22%3A%22k20%22%2C%22times%22%3A2%2C%22expires%22%3A%222019-07-11T09%3A14%3A32.024Z%22%7D%5D; customerCookie=vJUOdf+W6fJrKeRWC3NVwBv9+iLuBD+7DDjpy43Z5Nc=; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216b45d0db1160-03b4c9f2e-3b331f72-640200-16b45d0db1385%22%2C%22%24device_id%22%3A%2216b45d0db1160-03b4c9f2e-3b331f72-640200-16b45d0db1385%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
'X-Requested-With': 'com.cmbchina.ccd.pluto.cmbActivity'
}
num = 1
while True:
    try:
        r = requests.get(url, headers=headers)
        html = pq(r.text)
        strs = pq(html('.j_num')).text()
        if '已售罄' in strs:
            print('已查询{}次'.format(num))
            with open("zsyh.txt", "w", encoding='utf-8') as f:
                f.write('已查询{}次'.format(num))
            num += 1
            time.sleep(60)
        else:
            api = "https://sc.ftqq.com/SCU38261T75506f6dfae8ea68797927f27f59830e5c2340b46b2f6.send"
            data = {
                "text": '招商银行红米k20 pro有货啦',
                "desp": '招商银行红米k20 pro有货啦'
            }
            try:
                res = requests.post(api, data=data)
                if res.status_code == 200:
                    break
                else:
                    print('发送失败')
            except:
                print('Error: 发送出错')
    except:
        api = "https://sc.ftqq.com/SCU38261T75506f6dfae8ea68797927f27f59830e5c2340b46b2f6.send"
        data = {
            "text": '招商银行红米k20pro监控异常终止',
            "desp": '招商银行红米k20pro监控异常终止'
        }
        try:
            res = requests.post(api, data=data)
            if res.status_code == 200:
                break
            else:
                print('发送失败')
        except:
            print('Error: 发送出错')