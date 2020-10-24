import requests
from pyquery import PyQuery as pq
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import glob, os, time
import traceback

# 百分数转为int
def percent_to_int(string):
    if "%" in string:
        newint = int(string.strip("%")) / 100
        return newint
    else:
        print("你输入的不是百分比！")
        return 60

def download(title, durl, save_path):
    try:
        if '.mp4' in title:
            title = title
        else:
            title = '{}.mp4'.format(title)

        folder = os.path.exists('D:\KDW\1\{}'.format(title))
        # print('开始下载 - {}'.format(title))
        if folder:
            return {'code': 0, 'msg': '视频已存在 - {}'.format(title)}
        else:
            mp4 = requests.get(durl)
            with open('{}\{}'.format(save_path, title), "wb") as f:
                f.write(mp4.content)
            path_file_number = glob.glob('{}\*.mp4'.format(save_path))  # 或者指定文件下个数
            return {'code': 0, 'msg': '已下载{}部'.format(len(path_file_number))}
    except:
        return {'code': -1, 'msg': '下载失败 - {}'.format(title)}

def parse(res):
    res = res.result()
    print(res['msg'])

def get_durl(max):
    try:
        durls = []
        print('获取视频链接中，只下载评分高于70%的视频')
        for i in range(int(max)):
            url = 'http://www.xiaobi038.com/latest-updates/{}/'.format(i+1)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49'
                              ' Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080'
            }
            html = requests.get(url, headers=headers)
            items = pq(html.text)('#list_videos_latest_videos_list_items .item').items()
            for i, item in enumerate(items):
                # print(item)
                positive = item('a .positive').text()
                # 比较大小
                if percent_to_int(positive) > percent_to_int("80%"):
                    aurl = item('a').attr('href')
                    title = item('a').attr('title')
                    # added = item('a .wrap .added').text()
                    # views = item('a .wrap .views').text()
                    # print(i, aurl)
                    # print(title)
                    # print(positive)
                    # print(added)
                    # print(views)
                    html = requests.get(aurl, headers=headers)
                    items = pq(html.text)('#tab_video_info .block-details .info .item').items()
                    for i, item in enumerate(items):
                        if i == 4:
                            durl = item('a').attr('href')
                            # print('download: '+ durl)
                            # print('---------------------------------------')
                            dtup = (title, durl,)
                            durls.append(dtup)
        return durls
    except:
        print('获取视频链接异常，请稍后再试')
        print(traceback.format_exc())
        return -1

def main():
    max = input('请输入截止页数，默认从第一页开始下载：')
    durls = get_durl(max)
    if durls != -1:
        print('链接获取完毕，本次共有{}部视频待下载'.format(len(durls)))
        print('正在下载中，请稍后..视频保存文件夹为[D:\KDW]')
        save_path = r'D:\KDW\1'
        folder = os.path.exists(save_path)
        if not folder:
            os.makedirs(save_path)

        pool = ThreadPoolExecutor(5)

        for durl in durls:
            pool.submit(download, durl[0], durl[1], save_path).add_done_callback(parse)

main()


