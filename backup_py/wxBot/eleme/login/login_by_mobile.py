from bs4 import BeautifulSoup
import traceback
import re
import requests
from config.config import HEADERS, PROXIES, IS_DAILI

def login_by_mobile(validate_token, mobile, sms_url, conn, cursor, logger):  # 获取到短信验证码后登录，提取最新sid（身份认证信息）
    try:
        if len(sms_url) != 0: #该变量为空的话说明不是网上的接码平台号码 需手动输入短信验证码
            logger.info('[{}]正在获取短信验证码'.format(mobile))
            html = requests.get(sms_url, headers=HEADERS)
            if html.status_code == 200:
                Soup = BeautifulSoup(html.content, 'lxml')
                # print(aSoup)
                trList = Soup.find_all(name='tbody')[0].find_all(name='tr')
                if trList:
                    for tr in trList:
                        tdContent = tr.find_all(name='td')[2].string
                        if '【饿了么】' in tdContent:
                            validate_code = re.findall('验证码是(.*?)，', tdContent, re.S)[0]
                            logger.info('[{}]短信验证码识别成功,验证码为{}'.format(mobile, validate_code))
                            dict = {"mobile": "{}".format(mobile), "validate_token": "{}".format(validate_token),
                                    "validate_code": "{}".format(validate_code)}
                            login_by_mobile_url = 'https://h5.ele.me/restapi/eus/login/login_by_mobile'
                            r = requests.post(login_by_mobile_url, headers=HEADERS, data=dict,
                                              proxies=PROXIES if IS_DAILI else None, timeout=25)
                            if r.status_code == 200:
                                if 'SID' in r.cookies and 'USERID' in r.cookies:
                                    SID = r.cookies['SID']
                                    users_id = r.cookies['USERID']
                                    logger.info('[{}]获取成功，新的SID为[{}]，userid为[{}]'.format(mobile, SID, users_id))
                                    result = {'status': 0, 'sid': SID}
                                    cursor.execute("select mobile from eleme_id")
                                    id_values = str(cursor.fetchall())
                                    cursor.execute("select mobile from eleme_xh")
                                    xh_values = str(cursor.fetchall())
                                    if '{}'.format(mobile) in id_values:
                                        cursor.execute(
                                            "UPDATE eleme_id SET sid = '{}', users_id = '{}' WHERE mobile = '{}'".format(SID, users_id, mobile))
                                        conn.commit()
                                        logger.info('[{}]新的SID已写入成功_eleme_id'.format(mobile))
                                    if '{}'.format(mobile) in xh_values:
                                        cursor.execute("UPDATE eleme_xh SET sid = '{}', users_id = '{}' WHERE mobile = '{}'".format(SID, users_id, mobile))
                                        conn.commit()
                                        logger.info('[{}]新的SID已写入成功_eleme_xh'.format(mobile))
                                    return result
                                else:
                                    result = {'status': 1, 'message': '未找到，sid获取出错~{},{}'.format(r.text, r.cookies)}
                                    return result
                            else:
                                result = {'status': 1, 'message': '短信验证出错~{}'.format(
                                    r.text)}  # 这种情况一般是短信验证码错误，接码网站上最新的饿了么短信不是你前15秒发的，刚好也有人用此号码接了饿了么短信
                                return result
                        else:
                            result = {'status': 1, 'message': '未找到饿了么短信'}
                            return result
                else:
                    result = {'status': 1, 'message': 'trList列表为空'}
                    return result
            else:
                result = {'status': 1, 'message': '接码平台地址访问出错了~{}'.format(html.status_code)}
                return result
    except:
        result = {'status': 1, 'message': 'Error: {}'.format(traceback.format_exc())}
        return result