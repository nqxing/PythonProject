import requests
import time
import hashlib
import urllib.parse

def tenx_ai(question):
    app_id = 2116257824
    app_key = 'HyKfkoZ34CJoGJWy'
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'time_stamp': int(time.time()),
        'nonce_str': int(time.time()),
        'session': 10000,
        'question': question,
    }
    uri_str = ''
    for key in sorted(params.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, urllib.parse.quote(str(params[key]), safe=''))
    sign_str = uri_str + 'app_key=' + params['app_key']
    hash_md5 = hashlib.md5(sign_str.encode("latin1"))
    params['sign'] = hash_md5.hexdigest().upper()
    url_data = urllib.parse.urlencode(params).encode(encoding='utf-8')
    r = requests.get('https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat',params=url_data)
    if r.status_code == 200:
        if r.json()['ret'] == 0:
            return r.json()['data']['answer']
        else:
            return r.json()['msg']
    else:
        return '抱歉，出错了..'