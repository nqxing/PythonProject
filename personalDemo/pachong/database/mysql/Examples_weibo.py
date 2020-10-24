import requests
from pyquery import PyQuery as pq
def get_url(uid,page):
    params = {
        'type' : 'uid',
        'value' : '%s' % uid,
        'containerid' : '107603%s' % uid,
        'page' : '%s' % page
    }
    headers = {
        'host': 'm.weibo.cn',
        'referer': 'https: //m.weibo.cn/u/%s' % uid,
        'user - agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 67.0.3396.99 Safari / 537.36',
        'x - requested - with': 'XMLHttpRequest'
    }
    url = 'https://m.weibo.cn/api/container/getIndex?'
    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError as e:
        print("Error" ,e.args)

def parsing_url(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            text = pq(item.get('text')).text()  #正文
            timedata = item.get('created_at')  #发布时间
            attitudes = item.get('attitudes_count')  #点赞数
            comments = item.get('comments_count')   #评论数
            reposts = item.get('reposts_count')   #转发数
            abc(text,timedata,attitudes,comments,reposts)

def abc(text,timedata,attitudes,comments,reposts):
    print(text,timedata,attitudes,comments,reposts)

def main():
    for page in range(2,10):
        json = get_url(1223178222,page)
        parsing_url(json)
if __name__ == '__main__':
    main()