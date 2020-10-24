import requests
get_captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.6746513824427816'
captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
login_url = 'https://kyfw.12306.cn/passport/web/login'
uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
uamauthclient_url = 'https://kyfw.12306.cn/otn/uamauthclient'
def set_answer(answer):
    setAnswer = {
        '1': '37,38',
        '2': '110,38',
        '3': '180,38',
        '4': '250,38',
        '5': '37,118',
        '6': '110,118',
        '7': '180,118',
        '8': '250,118',
    }
    lists = []
    answerList = answer.split(',')
    for a in answerList:
        lis = setAnswer[a]
        lists.append(lis)
    return ','.join(lists)
session = requests.session()
headers = {
    'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36'
}
img = session.get(get_captcha_url, headers=headers)
with open("captcha.jpg", "wb") as f:
    f.write(img.content)
form_data = {
    'answer':set_answer(input("请输入验证码序号，多个用,号分隔: ")),
    'login_site':'E',
    'rand':'sjrand'
}
captcha_res = session.post(captcha_url,headers=headers,data=form_data).json()
if captcha_res['result_code'] == '4':
    f = open("userdata.txt", "r")
    lines = f.readlines()  # 读取全部内容
    userList = lines[0].strip().split(',')
    form_data = {
        'username': userList[0],
        'password': userList[1],
        'appid': 'otn'
    }
    login_res = session.post(login_url,headers=headers,data=form_data).json()
    if login_res['result_code'] == 0:
        uamtk_res = session.post(uamtk_url,headers=headers,data={'appid':'otn'}).json()
        if uamtk_res['result_code'] == 0:
            form_data = {
                'tk': uamtk_res['newapptk']
            }
            uamauthclient_res = session.post(uamauthclient_url,headers=headers,data=form_data).json()
            print(uamauthclient_res)
        else:
            print(uamtk_res['result_message'])
    else:
        print(login_res['result_message'])
else:
    print(captcha_res['result_message'])

