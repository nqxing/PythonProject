from auto_reply.models import pubLOLNews
from auto_reply.package import *

def cx_nid(tid):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    url = 'http://apps.game.qq.com/cmc/zmMcnTargetContentList?r0=jsonp&page=1&num=16&target={}&source=web_pc'.format(tid)
    news_ids = []
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r_json = re.findall('callback\((.*?)\);', r.text)
            if r_json:
                r_json = json.loads(r_json[0])
                if r_json['msg'] == 'OK':
                    results = r_json['data']['result']
                    for res in results:
                        res_dict = {}
                        # 加密
                        iDocID = bytes.decode(base64.b64encode(res['iDocID'].encode('utf-8')))
                        if tid == 23:
                            title = '【综合】' + res['sTitle']
                        elif tid == 24:
                            title = '【公告】' + res['sTitle']
                        elif tid == 25:
                            title = '【赛事】' + res['sTitle']
                        elif tid == 27:
                            title = '【攻略】' + res['sTitle']
                        else:
                            title = '【社区】' + res['sTitle']

                        values = pubLOLNews.objects.filter(doc_id=iDocID)
                        if values.exists():
                            pass
                        else:
                            if 'sVID' in res:
                                res_dict['sVID'] = True
                            if res['sRedirectURL']:
                                res_dict['sRedirectURL'] = res['sRedirectURL']
                            res_dict['iDocID'] = iDocID
                            res_dict['sTitle'] = title
                            news_ids.append(res_dict)
        return news_ids
    except:
        write_log(3, traceback.format_exc())
        return news_ids

def get_news_yxlm():
    num = 0
    tids = [23, 24, 25, 27, 28]
    for i in tids:
        results = cx_nid(i)
        if results:
            url = 'https://lol.qq.com/news/detail.shtml?docid={}'
            v_url = 'https://lol.qq.com/v/v2/detail.shtml?docid={}'
            for res in results:
                if 'sVID' in res:
                    link = v_url.format(bytes.decode(base64.b64decode(res['iDocID'])))
                elif 'sRedirectURL' in res:
                    link = res['sRedirectURL']
                else:
                    link = url.format(bytes.decode(base64.b64decode(res['iDocID'])))
                pub = pubVarList.objects.filter(var_name="LOL_NEW_NEWS")
                send_str = '{}|{}'.format(res['sTitle'], link)
                db_str = pub[0].var_info
                pubs = pub[0]
                if db_str != "None":
                    db_str += "${}".format(send_str)
                    pubs.var_info = db_str
                    pubs.save()
                else:
                    pubs.var_info = send_str
                    pubs.save()
                # send_fwx_group(WX_LOL_GROUPS, '{}\n{}'.format(res['sTitle'], link), True)
                # 英雄联盟暂无QQ群
                pub = pubLOLNews()
                pub.doc_id = res['iDocID']
                pub.news_title = res['sTitle']
                pub.news_title_url = link
                pub.save()
                time.sleep(1)
                num += 1
        time.sleep(5)
    write_log(1, '英雄联盟文章获取完毕，本次新增{}篇文章'.format(num))