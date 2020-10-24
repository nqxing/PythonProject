from robot.models import pubEleSignCode
from auto_reply.package import *

def new_browser(open_id, mobile):
    try:
        # 禁用此故障保护
        pg.FAILSAFE = False
        time.sleep(0.5)
        pg.hotkey('winleft', 'd')
        time.sleep(0.5)
        options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument(
            'user-agent="Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080"')
        browser = webdriver.Chrome(chrome_options=options)
        browser.maximize_window()
        url = "https://tb.ele.me/wow/msite/act/login?redirect=https%3A%2F%2Fh5.ele.me%2Fprofile%2F"
        browser.get(url)
        # print(browser.page_source)
        if browser.title != "手机号登录":
            for i in range(5):
                browser.refresh()  # 采用此方法刷新页面
                time.sleep(1)
                if browser.title == "手机号登录":
                    break
                if i == 4:
                    write_log(3, "{} - {} - 页面显示错误\n----------------\n{}\n----------------".format(open_id, mobile, browser.page_source))
                    return -1
        iframe = browser.find_element_by_id("alibaba-login-box")
        browser.switch_to.frame(iframe)
        browser.find_element_by_id("fm-sms-login-id").send_keys(mobile)
        time.sleep(1.5)
        browser.find_element_by_xpath("//*/a[text()='获取验证码']").click()
        try:
            locator = (By.ID, "nc_1_n1t")
            WebDriverWait(browser, 6).until(EC.presence_of_element_located(locator))
            write_log(1, "{} - {} - 需要滑动验证码".format(open_id, mobile))
        except:
            write_log(1, "{} - {} - 非滑动验证码验证\n----------------\n{}\n----------------".format(open_id, mobile, browser.page_source))
            return -1
        # 模拟人工滑动验证
        sliding()
        return browser
    except:
        write_log(3, traceback.format_exc())
        return -1

def sliding():
    # 模拟人工滑动验证
    pg.moveTo(210, 558, 1)
    pg.mouseDown()
    for i in range(210, 1825, 161):
        pg.moveTo(i, 558, duration=0.1)
    pg.mouseUp()
    time.sleep(1)

def get_cookie(open_id, mobile):
    try:
        values = pubEleSignCode.objects.filter(wx_open_id=open_id)
        if values.exists():
            pass
        else:
            pub = pubEleSignCode()
            pub.wx_open_id = open_id
            pub.save()
        sign_txt(open_id, "正在为您验证滑动验证码，请稍后..")
        # 查询当前是否有滑动动作，如果有就先等待
        hd_values = pubVarList.objects.filter(var_name="HD_VAL_STATE")
        hd = hd_values[0]
        if hd.var_info == "False":
            hd.var_info = "True"
            hd.save()
            browser = new_browser(open_id, mobile)
            if browser == -1:
                hd.var_info = "False"
                hd.save()
                result = {'status': -1, 'message': '-1,系统验证异常，请发送手机号重试'}
                return result
            hd.var_info = "False"
            hd.save()
        else:
            for i in range(300):
                hd_values = pubVarList.objects.filter(var_name="HD_VAL_STATE")
                hd = hd_values[0]
                if hd.var_info == "False":
                    break
                time.sleep(1)
                if i == 299:
                    write_log(3, "{} - {} - 后台验证超时了".format(open_id, mobile))
                    result = {'status': 3, 'message': "后台验证超时了，请重试"}
                    return result
            hd.var_info = "True"
            hd.save()
            browser = new_browser(open_id, mobile)
            if browser == -1:
                hd.var_info = "False"
                hd.save()
                result = {'status': -1, 'message': '-1,系统验证异常，请发送手机号重试'}
                return result
            hd.var_info = "False"
            hd.save()
        try:
            time.sleep(1.5)
            code_str = browser.find_elements_by_css_selector(".send-btn")[0].text
            if "重发" in code_str:
                result = save_sid(browser, open_id, mobile)
                return result
            else:
                sliding()
                time.sleep(1.5)
                code_str = browser.find_elements_by_css_selector(".send-btn")[0].text
                if "重发" in code_str:
                    result = save_sid(browser, open_id, mobile)
                    return result
                else:
                    write_log(3, "{} - {} - 验证码发送失败\n----------------\n{}\n----------------".format(open_id, mobile, browser.page_source))
                    browser.quit()
                    result = {'status': 1, 'message': '验证码发送失败，请重新发送手机号重试'}
                    return result
        except:
            write_log(3, "{} - {} - {}".format(open_id, mobile, traceback.format_exc()))
            browser.quit()
            result = {'status': -1, 'message': '系统验证异常，请发送手机号重试'}
            return result
    except:
        write_log(3, "{} - {} - {}".format(open_id, mobile, traceback.format_exc()))
        result = {'status': -1, 'message': '系统验证异常，请发送手机号重试'}
        return result

def save_sid(browser, open_id, mobile):
    values = pubEleSignCode.objects.filter(wx_open_id=open_id)
    value = values[0]
    value.is_send = True
    value.save()
    sign_txt(open_id, "滑动验证成功，验证码已发送，请回复验证码")
    write_log(1, "{} - {} - 验证码发送成功".format(open_id, mobile))
    for i in range(300):
        values = pubEleSignCode.objects.filter(wx_open_id=open_id)
        value = values[0]
        sms_code = value.sms_code
        if sms_code != '0':
            values = pubEleSignCode.objects.filter(wx_open_id=open_id)
            value = values[0]
            value.sms_code = "0"
            value.save()
            browser.find_element_by_id("fm-smscode").send_keys(sms_code)
            time.sleep(1.5)
            browser.find_element_by_xpath("//*/button[text()='同意协议并登录']").click()
            time.sleep(4)
            cookies = browser.get_cookies()
            USERID, SID = None, None
            for c in cookies:
                if c['name'] == 'USERID':
                    USERID = c['value']
                if c['name'] == 'SID':
                    SID = c['value']
            if USERID != None and SID != None:
                values = pubEleSignUsers.objects.filter(wx_open_id=open_id)
                if values.exists():
                    value = values[0]
                    value.mobile = mobile
                    value.sid = SID
                    value.user_id = USERID
                    value.is_bind = True
                    value.state = True
                    value.save()
                    browser.quit()
                    write_log(1, "{} - {} - 绑定成功[{},{}]".format(open_id, mobile, USERID, SID))
                    result = {'status': 0, 'message': "绑定成功"}
                    return result
                else:
                    write_log(3, "{} - {} - 1验证出现错误".format(open_id, mobile))
                    browser.quit()
                    result = {'status': 2, 'message': '验证出现错误，请发送手机号重试'}
                    return result
            else:
                write_log(3, "{} - {} - 2验证出现错误\n----------------\n{}\n----------------".format(open_id, mobile,
                                                                                                browser.page_source))
                browser.quit()
                result = {'status': 2, 'message': '验证出现错误，请重新发送手机号获取，请确认验证码输入正确，您输入的验证码为{}'.format(sms_code)}
                return result
        time.sleep(1)
    browser.quit()
    write_log(1, "{} - {} - 用户未发送验证码".format(open_id, mobile))
    result = {'status': 3, 'message': "您未在5分钟内发送验证码，本次验证已过期，请发送手机号重试"}
    return result