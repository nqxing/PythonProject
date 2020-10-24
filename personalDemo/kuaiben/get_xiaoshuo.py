from urllib import parse
import requests

def get_shum(sname):
    url = 'http://lunbo.gdugm.cn/search/suggest?key={}'.format(sname)
    r = requests.get(url)
    try:
        result = r.json()
        # print(result)
        if result['ok'] == True:
            keywords = result['keywords']
            print('--本次共找到{}本书籍--'.format(len(keywords)))
            for i in range(len(keywords)):
                if 'text' in keywords[i] and 'id' in keywords[i] and 'author' in keywords[i]:
                    print('书名：{}'.format(keywords[i]['text']))
                    print('id：{}'.format(keywords[i]['id']))
                    print('作者：{}'.format(keywords[i]['author']))
                    print()
        else:
            print('出错了')
    except:
        print('Error')

def get_zhangj(id):
    url = 'http://lunbo.gdugm.cn/toc/mix?bookId={}'.format(id)
    r = requests.get(url)
    try:
        result = r.json()
        if result['book'] == id:
            chapters = result['chapters']
            return chapters
        else:
            print('出错了')
    except:
        print('Error')

def get_content(link):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49'
                      ' Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080'
    }
    url = 'http://chapter.xmxingheju.com/chapter/{}'.format(parse.quote(link))
    r = requests.get(url, headers=HEADERS)
    try:
        result = r.json()
        if result['ok'] == True:
            chapter = result['chapter']
            return chapter['body']
            # print('{}'.format(chapter['body']))
        else:
            print('出错了')
    except:
        print('Error')


# get_shum('全球高武')
get_zhangj('5b1739ab4e66e33f75dca017')
# get_content('http://book.kdqb.cc/getBooks.aspx?method=content&bookId=42033&chapterFile=U_42033_201903291542285496_1308_1.txt')