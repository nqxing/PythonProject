from auto_reply.models import pubKeys
from auto_reply.package import *

def return_keyInfo(key_text):
    try:
        results = pubKeys.objects.filter(key__contains=key_text)
        if len(results) != 0:
            result = '找到了{}个和({})有关的内容哦\n\n'.format(len(results), key_text)
            for res in results:
                strs = '{}\n\n'.format(res.key_info)
                result += strs
            return result.strip()
        else:
            return 0
    except:
        write_log(3, '{}'.format(traceback.format_exc()))
        return "抱歉~ 查询出错了，请重试~"
