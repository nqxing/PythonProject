import requests

headers = {
    "Host": "game.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "content-type": "application/json",
    "Referer": "https://servicewechat.com/wx4a0a73ec028e47d7/102/page-frame.html",
}

data = {
    "code": "0218oiqo1t0Gil0VbQoo1PIeqo18oiq9",
    "need_openid": True
}

response = requests.post("https://game.weixin.qq.com/cgi-bin/gameweappauthwap/login", headers=headers, data=data, verify=False)
print(response.text)