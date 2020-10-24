import requests
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
            pass
        else:
            print('发送失败')
    except:
        print('Error: 发送出错')