from django.views import View
from django.http import HttpResponse
from auto_reply.reply.ele_sign import ele_sign_reply
from auto_reply.package import *

class BindEleSignMobile(View):
    def get(self, request):
        try:
            eleme_sign_dict = {}
            fromUser = request.GET.get("fromUser")
            types = request.GET.get("type")
            content = request.GET.get("content")
            if types == 'mobile':
                eleme_sign_dict[fromUser] = 'mobile'
                res = ele_sign_reply(eleme_sign_dict, None, eleme_sign_cap_dict_api, fromUser, content, "", False)
            elif types == 'captcha':
                eleme_sign_dict[fromUser] = 'captcha'
                res = ele_sign_reply(eleme_sign_dict, None, eleme_sign_cap_dict_api, fromUser, content, "", False)
            elif types == 'codenum':
                eleme_sign_dict[fromUser] = 'codenum'
                res = ele_sign_reply(eleme_sign_dict, None, eleme_sign_cap_dict_api, fromUser, content, "", False)
            elif types == 'codenum_hd':
                eleme_sign_dict[fromUser] = 'codenum_hd'
                res = ele_sign_reply(eleme_sign_dict, None, eleme_sign_cap_dict_api, fromUser, content, "", False)
            else:
                res = "系统异常，请稍后再试"
            if "若需重新发送手机号" in res:
                res = res.replace('2', '修改手机号')
            return HttpResponse(res)
        except:
            write_log(3, format(traceback.format_exc()))
            return HttpResponse("系统异常，请稍后再试")