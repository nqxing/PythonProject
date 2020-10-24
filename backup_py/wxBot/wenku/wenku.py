import traceback
import requests
import json
import re
from pyquery import PyQuery as pq
import datetime

def get_cookie():#获取域名访问所需要的__cfduid值
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language":"zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
        "Accept-Encoding": "gzip, deflate",
        "Host":"www.blpack.com",
        "Connection": "Keep-Alive"
    }
    res = requests.get("http://www.blpack.com/", headers=header)
    cookie = res.headers["Set-Cookie"]
    cookie = re.findall("uid=(.*?);", cookie)
    return cookie[0]

def GET_SHORTURL(firsturl):
    try:
        def get_long_url():
            # usrname_list = ["160414436", "901961495"]
            # usrpwd_list =["095024", "559448"]
            f = open(r"C:\PythonProject\wxBot\wenku\id.txt", "r", )
            lines = f.readlines()  # 读取全部内容
            for i in range(len(lines)):
                datas = lines[i].strip().split(',')
                usrname = datas[0]
                usrpwd = datas[1]
                # print(usrname, usrpwd)
                url1 = "http://www.blpack.com/post.php"# 以下用到了两个链接，一个是查询文档ID的，另一个是下载的
                url3 = "http://www.blpack.com/downdoc.php"
                # 将传入的文档链接进行转化
                downloadurl = firsturl.replace("/", "%2F").replace(":", "%3A")
                __cfduid = get_cookie()

                def query(): #查询文档ID
                    head1 = {"POST": "http://www.blpack.com/post.php HTTP/1.1",
                             "Host": "www.blpack.com",
                             "Content-Length": "145",
                             "Accept": "*/*",
                             "Origin": "http://www.blpack.com",
                             "X-Requested-With": "XMLHttpRequest",
                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                             "Referer": "http://www.blpack.com/",
                             "Accept-Encoding": "gzip, deflate",
                             "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                             "Cookie": "__cfduid={}; usrname={}; usrpwd={}".format(__cfduid, usrname, usrpwd)
                             }
                    data1 = 'usrname={}&usrpass={}&docinfo={}&taskid=up_down_doc1'.format(usrname, usrpwd, downloadurl)
                    respons = requests.post(url1, data=data1, headers=head1).json()
                    id = respons['url']
                    id = id[36:]  #将response的链接截取id值
                    return id

                def down():  # 获取下载链接
                    id = query()
                    Referer = "http://www.blpack.com/nocode.php?id={docid}"
                    head3 = {"POST": "http://www.blpack.com/downdoc.php HTTP/1.1",
                             "Host": "www.blpack.com",
                             "Connection": "keep-alive",
                             "Content-Length": "54",
                             "Accept": "*/*",
                             "Origin": "http://www.blpack.com",
                             "X-Requested-With": "XMLHttpRequest",
                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                             "Referer": Referer.format(docid=id),
                             "Accept-Encoding": "gzip, deflate",
                             "Accept-Language": "zh-CN,zh;q=0.9",
                             "Cookie": "__cfduid={}; usrname={}; usrpwd={}".format(__cfduid, usrname, usrpwd)
                             }
                    data3 = 'vid={docid}&taskid=directDown'.format(docid=id)
                    response = requests.post(url3, data=data3, headers=head3).json()
                    if response["result"]=="down_succ":
                        downurl = response["dlink"]  #获取下载长链接
                        return downurl
                    else:
                        downurl = response["msg"]
                        return downurl
                downurl = down()
                if downurl[0:5]=="https":  #判断账号是否可用，可用进行下一步
                    file_url = download(downurl, firsturl)
                    if file_url != False:
                        dwzUrl = short_url("http://ele.379lb.cn/wenku/{}".format(file_url))
                        return dwzUrl
                    else:
                        with open(r'wenku\url.txt', 'a', encoding='utf-8') as file:
                            file.write("{} - {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), downurl))
                        return '系统转存失败，请重新发送'
                elif i == len(lines)-1:
                    # back = "所有账号均不可用"
                    return downurl
                # else:
                #     i += 1

        def short_url(long_url): #将长链接变成短链接
            host = 'https://dwz.cn'
            path = '/admin/v2/create'
            url = host + path
            url1 = long_url
            content_type = 'application/json'
            # TODO: 设置Token
            token = '9b2b162c0770cbba0da6c1cbcee36f54'  #访问"https://dwz.cn/console/userinfo"登录百度账号，即可免费获取令牌
            # TODO：设置待创建的长网址
            bodys = {'url': url1, 'TermOfValidity': '1-year'}
            # 配置headers
            headers = {'Content-Type': content_type, 'Token': token}
            # 发起请求
            response = requests.post(url=url, data=json.dumps(bodys), headers=headers).json()
            # 读取响应
            if response['Code'] == 0:
                return response["ShortUrl"]
            else:
                return url1

        long_url = get_long_url()
        if long_url[0:5] == "https": #判断是否获得长链接，是则下一步
            res = short_url(long_url)
            return '处理完毕，下载链接为：{}'.format(res)
        else:
            # print(long_url)
            return long_url
    except:
        # print(traceback.format_exc())
        r = "获取下载链接失败，请检查是否是付费文档，或者地址是否正确"
        return r

def get_wenku(text, msg):
    if '//wk.baidu.com' in text:
        text = text.replace('//wk.baidu.com', '//wenku.baidu.com')
    msg.reply('已识别到百度文库链接，正在为你处理，请稍等...')
    result = GET_SHORTURL(text)
    msg.reply(result)

def get_title(title_url):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    try:
        r = requests.get(title_url, headers=headers)
        r.encoding = 'gb2312'
        html = pq(r.text)
        h1 = html('h1')
        suffixs = h1('b').attr('class')
        title = h1('span').text()
        if len(title) != 0:
            if 'doc' in suffixs:
                suffix = '.doc'
            elif 'docx' in suffixs:
                suffix = '.docx'
            elif 'xls' in suffixs:
                suffix = '.xls'
            elif 'xlsx' in suffixs:
                suffix = '.xlsx'
            elif 'pdf' in suffixs:
                suffix = '.pdf'
            elif 'ppt' in suffixs:
                suffix = '.ppt'
            elif 'pptx' in suffixs:
                suffix = '.pptx'
            else:
                suffix = '.未知后缀'
            return title + suffix
        else:
            suffix = '文件名获取失败请手动加文件后缀'
            return suffix
    except:
        suffix = '文件名获取失败请手动加文件后缀'
        return suffix

def download(url, title_url):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    try:
        file = requests.get(url, headers = headers)
        if file.status_code == 200:
            title = get_title(title_url)
            with open(r"C:\inetpub\wwwroot\wenku\{}".format(title), "wb") as f:
                f.write(file.content)
            return title
        else:
            return False
    except:
        return False
# url = 'https://wkbjcloudbos.bdimg.com/v1/wenku21//7d73123c3b23ce15f651e593f2c1eaf9?responseContentDisposition=attachment%3B%20filename%3D%22H3C-track%25E9%2585%258D%25E7%25BD%25AE%25E6%2589%258B%25E5%2586%258C.pdf%22%3B%20filename%2A%3Dutf-8%27%27H3C-track%25E9%2585%258D%25E7%25BD%25AE%25E6%2589%258B%25E5%2586%258C.pdf&responseContentType=application%2Foctet-stream&responseCacheControl=no-cache&authorization=bce-auth-v1%2Ffa1126e91489401fa7cc85045ce7179e%2F2019-11-13T05%3A20%3A28Z%2F3000%2Fhost%2Ffdaa0c905cbbcc75140f37dd50d8aea044ed633382c113697cd3b71b3a5d5786&token=eyJ0eXAiOiJKSVQiLCJ2ZXIiOiIxLjAiLCJhbGciOiJIUzI1NiIsImV4cCI6MTU3MzYyNTQyOCwidXJpIjp0cnVlLCJwYXJhbXMiOlsicmVzcG9uc2VDb250ZW50RGlzcG9zaXRpb24iLCJyZXNwb25zZUNvbnRlbnRUeXBlIiwicmVzcG9uc2VDYWNoZUNvbnRyb2wiXX0%3D.NsSLqklDseFuB3PgbxQCHXFDr9dBT8nwbwGNjiybLWk%3D.1573625428'
# download(url)