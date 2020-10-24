from auto_reply.models import pubWZNews
from auto_reply.package import *

def cx_nid(tid):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    url = 'http://apps.game.qq.com/wmp/v3.1/'
    dict = {
    'p0': 18,
    'p1': 'searchNewsKeywordsList',
    'order': 'sIdxTime',
    'r0': 'cors',
    'type': 'iTarget',
    'source': 'app_news_search',
    'pagesize': 12,
    'page': 1,
    'id': tid,
    }
    news_ids = []
    try:
        r = requests.post(url, data=dict, headers=headers)
        if r.status_code == 200:
            r_json = r.json()
            if r_json['status'] == '0':
                results = r_json['msg']['result']
                for res in results:
                    iNewsId = res['iNewsId']
                    if tid == 1761:
                        title = '【新闻】' + res['sTitle']
                    elif tid == 1762:
                        title = '【公告】' + res['sTitle']
                    elif tid == 1763:
                        title = '【活动】' + res['sTitle']
                    else:
                        title = '【赛事】' + res['sTitle']
                    values = pubWZNews.objects.filter(doc_id=iNewsId, news_title=title)
                    if values.exists():
                        pass
                    else:
                        news_ids.append({'iNewsId': iNewsId, 'sTitle': title})
        return news_ids
    except:
        write_log(3, traceback.format_exc())
        return news_ids

def get_news_wzry():
    num = 0
    for i in range(1761, 1765):
        results = cx_nid(i)
        if results:
            url = 'https://pvp.qq.com/web201706/newsdetail.shtml?tid={}'
            for res in results:
                if is_yingdi(res['iNewsId']):
                    link = 'https://image.ttwz.qq.com/h5/webdist/info-detail.html?iInfoId=180{}'.format(res['iNewsId'])
                else:
                    link = url.format(res['iNewsId'])
                title = res['sTitle']
                send_str = r'{}|{}'.format(title, link)
                pub = pubVarList.objects.filter(var_name="WZ_NEW_NEWS")
                db_str = pub[0].var_info
                pubs = pub[0]
                if db_str != "None":
                    db_str += "${}".format(send_str)
                    pubs.var_info = db_str
                    pubs.save()
                else:
                    pubs.var_info = send_str
                    pubs.save()
                # send_fwx_group(WX_WZ_GROUPS, send_str, True)

                # 20201016因酷Q关闭服务，关闭QQ发送通道
                # send_fqq_group(send_str)
                pub = pubWZNews()
                pub.doc_id = res['iNewsId']
                pub.news_title = title
                pub.news_title_url = link
                pub.save()
                time.sleep(1)
                num += 1
        time.sleep(5)
    write_log(1, '王者荣耀文章获取完毕，本次新增{}篇文章'.format(num))

def is_yingdi(iInfoId):
    url = 'https://ssl.kohsocialapp.qq.com:10001/game/detailinfov4'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    dict = {
        'iInfoId': int('180'+iInfoId),
        'cSystem': 1,
        'apiVersion': 4,
        'gameId': 20001,
        # 'msdkToken':'',
        # 'h5Get':1,
    }
    try:
        r = requests.post(url, data=dict, headers=headers)
        if r.json()['returnCode'] == 0:
            return True
        else:
            return False
    except:
        write_log(3, traceback.format_exc())
        return False