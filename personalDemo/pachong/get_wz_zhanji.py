import requests

cookies = {
    # 'eas_sid': '61v5C7M0Q7r7M4g91131S9K5p3',
    # 'pgv_pvid': '5680390386',
    # 'RK': 'KDRo5o2oMu',
    # 'ptcz': '86df9af3f452cd5fa366345866a75be10609ac3fda6ca80c5c8f945d4c0c5cb6',
    # 'pgv_pvi': '3783015424',
    # 'TGLoginJSCurDomain': 'tgideas.qq.com',
    # 'ied_qq': 'o0541116212',
    # 'LW_uid': '01T5N8X7V5T3l747o7k9f7A7c1',
    # 'LW_sid': 'W1q578o7I9v8h2c0H6q0O1Z3j4',
    # 'cookie_passkey': '1',
    'uin': 'Nzc0MjkzNTIy',
    'key': '20868f5ee1cf31c53bf2ae3f49f8758f58b25a3d0ba0046d14fc251b4ac647d6db28e068907e2bf3f586797bbc3aceefeb2205fb5ca5a9af5002ce4501f1c58ab7a4555e30a23924224e44ecd3d6cd0e',
    'pass_ticket': 'FoFxUo0lq6d00H1TEFD%2BhRkFqwIo7zMhdygL8ctFSvlDV5FHD2lsUOm9%2BfSvc%2BBG',
}

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://game.weixin.qq.com/cgi-bin/h5/static/smobadynamic/profile.html',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    ('openid', 'owanlsnwgESzThKU_Dgc6Fu0Z-II'),
    ('needLogin', 'true'),
    ('method', 'GET'),
    ('abtest_cookie', ''),
    ('abt', ''),
    ('QB', ''),
    ('', ''),
)

response = requests.get('https://game.weixin.qq.com/cgi-bin/gamewap/getsmobarecordprofile', headers=headers, params=params, cookies=cookies)
print(response.text)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://game.weixin.qq.com/cgi-bin/gamewap/getsmobarecordprofile?needLogin=true&method=GET&abtest_cookie=&abt=&QB&', headers=headers, cookies=cookies)
