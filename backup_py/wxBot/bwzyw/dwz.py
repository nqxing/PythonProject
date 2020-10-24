import requests
import re, sqlite3

def sina():
    url = 'https://gitee.com/Kuain2013/Short-Url/raw/master/PlugList.json'
    get_url = 'https://service.weibo.com/share/share.php?url={}&pic=pic&appkey=key&title={}'.format(url, url)
    r = requests.get(get_url)
    r.encoding = 'utf-8'
    print(r.text)
    dwzs = re.findall('scope.short_url = "(.*?)";', r.text, re.S)
    print(dwzs)
    if dwzs:
        print(dwzs[0].strip())


def tencent(urls):
    url = "https://vip.video.qq.com/fcgi-bin/comm_cgi"
    dict = {
        'name' : "short_url",
        'need_short_url': '1',
        'url': '{}'.format(urls)
    }
    try:
        r = requests.get(url, data=dict)
        print(r.text, r.status_code)
        if 'ok' in r.text and 'short_url' in r.text:
            return r.text
        else:
            return -1
    except:
        return -1

def tencent1(urls):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080',
        'Content-Type':'text/html; charset=UTF-8'
    }
    url = "http://dwz.2xb.cn/t?url={}".format(urls)
    # url = "http://dwz.2xb.cn/wurl?url={}".format(urls)
    dict = {
        'url': '{}'.format(urls)
    }
    try:
        r = requests.post(url).json()
        print(r)
        # if 'ok' in r.text and 'short_url' in r.text:
        #     return r.text
        # else:
        #     return -1
    except:
        return -1

# tencent1("https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/518/518-mobileskin-3.jpg")


def souim(urls):
    url = "http://suo.im/api.htm?url={}&key=5d68979fb1a9c70269346191@8b1adc61fdc362158a352a191513e054&expireType=6".format(urls)
    try:
        r = requests.get(url).text
        print(r)
        # if 'ok' in r.text and 'short_url' in r.text:
        #     return r.text
        # else:
        #     return -1
    except:
        return -1


souim("https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/518/518-mobileskin-3.jpg")
# tencent("https%3a%2f%2fwww.52pojie.cn%2fthread-1163267-1-1.html")
# sina()
# num = 1
# conn = sqlite3.connect(r'C:\PythonProject\wxBot\bizhi\wzry\wzry.db')
# # 创建一个游标 curson
# cursor = conn.cursor()
# cursor.execute("alter table pf_link add dwz_url varchar(255);")
# conn.commit()
# cursor.execute("SELECT id,pf_link FROM pf_link")
# results = cursor.fetchall()
# for res in results:
#     result = tencent(res[1])
#     if result != -1:
#         short_url = re.findall('"short_url" : "(.*?)"', result)[0]
#         print(num, short_url)
#         cursor.execute("UPDATE pf_link SET dwz_url = '{}' WHERE id = {}".format(short_url, res[0]))
#         conn.commit()
#         num += 1
#     else:
#         print(res)

# def qr_url():
#     url = 'https://tenapi.cn/qr?txt={}'.format("http://baidu.com")
#     r = requests.get(url)
#     with open(r"1.png".format(r), "wb") as f:
#         f.write(r.content)
#     print(r.status_code)
# qr_url()