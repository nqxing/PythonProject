from pub_zqwz.config import *

# 转换短网址
def short_url_new(urls):
    short_link = short_zuiqu(urls)
    if short_link != -1:
        return short_link
    else:
        return urls

def short_zuiqu(urls):
    dict = {
        "long": urls,
        "period": "长期"
    }
    try:
        r = requests.post("http://127.0.0.1:90/s/addShortUrl/", data=dict).json()
        if r['status'] == 100:
            return 'http://zuiqu.net/s/{}'.format(r['msg'])
        else:
            return -1
    except:
        log(3, traceback.format_exc())
        return -1

def fangtang(title, content):
    api = "https://sc.ftqq.com/SCU38261T75506f6dfae8ea68797927f27f59830e5c2340b46b2f6.send"
    data = {
        # "sendkey": "7639-5d73449e8a2a1db47195cfc57210c07a",
        "text": title,
        "desp": content
    }
    try:
        res = requests.post(api, data=data)
        if res.status_code == 200:
            log(1, '方糖通知发送成功')
        else:
            log(1, '方糖通知发送失败')
    except:
        log(3, traceback.format_exc())