from auto_reply.package import *
from .ele_sign_login import mobile_send_code, login_by_mobile
from .ele_sign_login_selenium import get_cookie
from .ele_sign_run import send_sign_index
from robot.models import pubEleSignUsers, pubEleSignVdtoken, pubEleSignCode


class my_thread(threading.Thread):
    def __init__(self, eleme_sign_dict, openId, mobile, state):
        threading.Thread.__init__(self)
        self.eleme_sign_dict = eleme_sign_dict
        self.openId = openId
        self.mobile = mobile
        self.state = state
    def run(self):
        eleme_sign_verify_mobile_hd(self.eleme_sign_dict, self.openId, self.mobile, self.state)
def eleme_sign_verify_mobile_hd_index(eleme_sign_dict, openId, mobile, state):
    th = my_thread(eleme_sign_dict, openId, mobile, state)
    th.start()

def eleme_sign_open(openId):
    values = pubEleSignUsers.objects.filter(wx_open_id=openId)
    if values.exists():
        value = values[0]
        mobile = value.mobile
        state = value.state
        if state and mobile == None:
            return '您已开启饿了么自动签到，但还未绑定手机号，现在回复手机号绑定吧'
        elif not state and mobile == None:
            value.state = True
            value.save()
            return '您已开启饿了么自动签到，但还未绑定手机号，现在回复手机号绑定吧'
        elif not state and mobile != None:
            value.state = True
            value.save()
            return '您的饿了么自动签到开启成功，当前绑定的手机号为（{}），如需更改请在5分钟内回复你要修改的手机号\n\n回复1：绑定微信/QQ发送签到结果\n回复2：关闭饿了么自动签到\n回复3：删除并关闭饿了么签到'.format(mobile)
        else:
            return '您已开启饿了么自动签到，当前绑定的手机号为（{}），如需更改请在5分钟内回复你要修改的手机号\n\n回复1：绑定微信/QQ发送签到结果\n回复2：关闭饿了么自动签到\n回复3：删除并关闭饿了么签到'.format(mobile)
    else:
        eleSign = pubEleSignUsers()
        eleSign.wx_open_id = openId
        eleSign.save()
        values = pubEleSignUsers.objects.filter(wx_open_id=openId)
        if values.exists():
            return '您的饿了么自动签到已开启，因你是首次开启需要绑定手机号，请在5分钟内回复你要签到的手机号'
        else:
            return '饿了么签到开启失败，请稍后再试'

def eleme_sign_close(openId):
    values = pubEleSignUsers.objects.filter(wx_open_id=openId)
    if values.exists():
        value = values[0]
        state_str = value.state
        if state_str:
            value.state = False
            value.save()
            return '您的饿了么自动签到已关闭，系统将不会再为你自动签到'
        if not state_str:
            return '您的饿了么自动签到已是关闭状态，无需重复关闭'
    else:
        return '您未开启饿了么自动签到，无需关闭'

def eleme_sign_del_close(openId):
    values = pubEleSignUsers.objects.filter(wx_open_id=openId)
    if values.exists():
        value = values[0]
        value.wx_open_id = "DEL_{}".format(openId)
        value.bind_name = "DEL"
        value.wx_note = "DEL"
        value.qq = "DEL"
        value.state = False
        value.is_bind = False
        value.save()
        return '删除成功，系统将不会再为你自动签到'
    else:
        return '您未开启饿了么自动签到，无需删除'

def eleme_sign_verify_mobile(openId, mobile):
    values = pubEleSignUsers.objects.filter(wx_open_id=openId)
    if values.exists():
        def is_mobile(mobile):
            if '13' == mobile[0:2]:
                return True
            elif '14' == mobile[0:2]:
                return True
            elif '15' == mobile[0:2]:
                return True
            elif '16' == mobile[0:2]:
                return True
            elif '17' == mobile[0:2]:
                return True
            elif '18' == mobile[0:2]:
                return True
            elif '19' == mobile[0:2]:
                return True
            else:
                return False
        if len(mobile) == 11:
            if is_mobile(mobile):
                result = mobile_send_code(openId, mobile)
                if result['status'] == 0:
                    values = pubEleSignVdtoken.objects.filter(wx_open_id=openId)
                    mobile = result['mobile']
                    validate_token = result['validate_token']
                    if values.exists():
                        value = values[0]
                        value.mobile = mobile
                        value.vdtoken = validate_token
                        value.save()
                    else:
                        eleVdtoken = pubEleSignVdtoken()
                        eleVdtoken.wx_open_id = openId
                        eleVdtoken.mobile = mobile
                        eleVdtoken.vdtoken = validate_token
                        eleVdtoken.save()
                    return result
                elif result['status'] == 1:
                    return result
                else:
                    return result
            else:
                result = {'status': 2, 'message': '请发送正确的手机号'}
                return result
        else:
            result = {'status': 2, 'message': '请发送正确的手机号'}
            return result
    else:
        result = {'status': 3, 'message': '您未开启饿了么自动签到，无需绑定手机'}
        return result

def eleme_sign_verify_code(openId, validate_code):
    try:
        if len(validate_code) == 6 and validate_code.isdigit():
            values = pubEleSignUsers.objects.filter(wx_open_id=openId)
            if values.exists():
                vd_values = pubEleSignVdtoken.objects.filter(wx_open_id=openId)
                if vd_values.exists():
                    result = login_by_mobile(validate_code, vd_values[0].vdtoken, vd_values[0].mobile)
                    if result['status'] == 0:
                        value = values[0]
                        value.mobile = vd_values[0].mobile
                        value.sid = result['sid']
                        value.user_id = result['users_id']
                        value.is_bind = True
                        value.state = True
                        value.save()
                        result = {'status': 0}
                        return result
                    else:
                        return result
            else:
                result = {'status': -1, 'message': '验证出现错误，请重新发送验证码试试吧'}
                return result
        else:
            result = {'status': 2, 'message': '输入错误，验证码为6位数字哦，请重新发送'}
            return result
    except:
        write_log(3, '{}'.format(traceback.format_exc()))
        result = {'status': -1, 'message': '验证出现错误，请重新发送验证码试试吧'}
        return result
    
def eleme_sign_verify_mobile_hd(eleme_sign_dict, open_id, mobile, state):
    result = get_cookie(open_id, mobile)
    if result['status'] == 0:
        sign_txt(open_id, result['message'])
        send_sign_index(open_id, False)
    else:
        sign_txt(open_id, result['message'])
        if state:
            eleme_sign_dict[open_id] = 'mobile'
    values = pubEleSignCode.objects.filter(wx_open_id=open_id)
    value = values[0]
    value.is_send = False
    value.save()