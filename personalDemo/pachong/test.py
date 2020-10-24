def test6():
    # 双列表同时循环方法
    list1 = [1, 2, 3, 4]
    list2 = [5, 6, 7, 8]
    for (i1, i2) in zip(list1, list2):
        i3 = i1 + i2
        print(i3)

def test12():
    from fake_useragent import UserAgent
    ua = UserAgent()
    print(ua.ie)  # 随机打印ie浏览器任意版本
    print(ua.firefox)  # 随机打印firefox浏览器任意版本
    print(ua.chrome)  # 随机打印chrome浏览器任意版本
    print(ua.random)  # 随机打印任意厂家的浏览器

def test9():
    import os
    # 创建文件夹
    def mkdir(path):
        folder = os.path.exists(path)

        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
            print("创建新文件夹")

            print("创建成功")
        else:
            print("该文件夹已经存在")

def test1():
    # 实时打印结果 替换上个变量
    import time
    import sys
    int1 = 50
    start = time.time()
    print('当前：',int(start))
    for i in range(50):
        sys.stdout.write('\r')
        # sys.stdout.write("%s%% 正在下载%s" % (int(i % 101), int(i % 6) * '.'))
        sys.stdout.write('正在下载%s %s/%s' % (int(i % 6) * '.',i,int1))
        sys.stdout.flush()
        time.sleep(0.1)

    sys.stdout.write('\n')
    print('最后：',int(time.time()))
    a = int(time.time()-start)
    print('相减：',a)
    print('%s时%s分%s秒~~'%(int(a/3600),int(int(a%3600)/60),int(a%3600)%60))
    # print(a/3600+'时'+(a-int(a/3600)*3600)/60+'分'+a-(a-int(a/3600)*3600)/60*60+'秒')

def test2():
    # 转为sha1加密
    from hashlib import sha1
    psw = sha1()
    psw.update("你好啊".encode('utf8'))
    spwdSha1 = psw.hexdigest()
    print(spwdSha1)

    psw.update("你好不啊".encode('utf8'))
    spwdSha1 = psw.hexdigest()
    print(spwdSha1)

def test3():
    # 保存二进制文件 如：图片 音乐 视频
    import requests
    img_path = 'D:/'
    img_name = 'baiyang'
    r = requests.get("http://music.163.com/song/media/outer/url?id=514761281.mp3")
    with open(img_path + '/' + img_name + '.mp3', "wb") as f:
        f.write(r.content)

def test4():
    # 多线程方法，开启多线程访问贴吧
    import requests
    from multiprocessing.dummy import Pool as ThreadPool
    import time
    def getsource(url):
        html = requests.get(url)
        print(html.status_code)
    if __name__ == '__main__':
        urls = []
        for i in range(50, 500, 50):
            newpage = 'http://tieba.baidu.com/f?kw=python&ie=utf-8&pn=' + str(i)
            urls.append(newpage)
        # # 单线程计时
        # time1 = time.time()
        # for i in urls:
        #     # print(i)
        #     getsource(i)
        # time2 = time.time()
        #
        # print('单线程耗时 : ' + str(time2 - time1) + ' s')

        # 多线程计时
        pool = ThreadPool(4)
        time3 = time.time()
        results = pool.map(getsource, urls)
        pool.close()
        pool.join()
        time4 = time.time()
        print('多线程耗时 : ' + str(time4 - time3) + ' s')

def test5():
    # 多线程方法

    # 单线程
    # import time
    # def sayhello(str):
    #     print("Hello ",str)
    #     time.sleep(2)
    #
    # name_list =['xiaozi','aa','bb','cc']
    # start_time = time.time()
    # for i in range(len(name_list)):
    #     sayhello(name_list[i])
    # print('%d second'% (time.time()-start_time))

    # 多线程
    import time
    import threadpool
    def sayhello(str):
        print("Hello ", str)
        time.sleep(2)

    name_list = ['xiaozi', 'aa', 'bb', 'cc']
    start_time = time.time()
    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(sayhello, name_list)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    print('%d second' % (time.time() - start_time))

def test7():
    # 发送邮件
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    # 第三方 SMTP 服务
    mail_host = "smtp.126.com"  # 设置服务器
    mail_user = "kqinxing@126.com"  # 用户名
    mail_pass = "qq184417622"  # 口令

    sender = 'kqinxing@126.com'
    receivers = ['kqinxing@126.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText('快去抢票啦...', 'plain', 'utf-8')
    message['From'] = Header("话多会腻", 'utf-8')
    message['To'] = Header("NQXing", 'utf-8')

    subject = '快去抢票啦~~'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
        print("Error: 无法发送邮件")

def test8():
    # 发送微信消息
    import itchat

    def send_move():
        # nickname = input('please input your firends\' nickname : ' )
        #   想给谁发信息，先查找到这个朋友,name后填微信备注即可,deepin测试成功
        # users = itchat.search_friends(name=nickname)
        users = itchat.search_friends(name='小号')  # 使用备注名来查找实际用户名
        # 获取好友全部信息,返回一个列表,列表内是一个字典
        print(users)
        # 获取`UserName`,用于发送消息
        userName = users[0]['UserName']
        itchat.send("该起来动一下了！！！", toUserName=userName)
        print('succeed')

    if __name__ == '__main__':
        itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录
        send_move()

def test10():
    # svn跳过身份认证
    import requests
    # headers = {
    #     "Host":"58.22.30.37:4433",
    #     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    # }
    r = requests.get('http://58.22.30.37:4433/!/#TestCase', auth=("nieqinxing", "231798"))
    print(r.status_code)
    print(r.text)

def test11():
    # 字符串和数字组合 按数字大小排序
    import re

    def sort_key(s):
        # 排序关键字匹配
        # 匹配数字序号
        if s:
            try:
                c = re.findall(r'(\d+)', s)[0]
            except:
                c = -1
            return int(c)

    def strsort(alist):
        alist.sort(key=sort_key)
        return alist

    if __name__ == "__main__":
        a = ['高二17班', '高二1班', '高二18班', '高二16班', '高二13班', '高二9班', '高二2班', '高二14班', '高二8班', '高二3班', '高二4班', '高二11班',
             '高二5班',
             '高二15班', '高二6班', '高二10班', '高二7班', '高二班12']

        print(strsort(a))