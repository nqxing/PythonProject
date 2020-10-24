import requests
get_captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.6746513824427816'
session = requests.session()
img = session.get(get_captcha_url,)
with open("captcha.jpg", "wb") as f:
    f.write(img.content)