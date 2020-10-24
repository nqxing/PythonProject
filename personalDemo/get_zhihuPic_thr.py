import requests
import re
import os
import time
from threading import Thread
import threadpool
import traceback
import sys
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
class getZhiHuPic:
    def __init__(self):
        self.id = 305040147
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        self.zh_id = 1
        self.zx_id = 1
        self.nm_id = 1
        self.cz_id = 1
        self.path = "D:/知乎答案图片/{}"
    def get_offset(self):
        url = 'https://www.zhihu.com/api/v4/questions/{}/answers'.format(self.id)
        r = requests.get(url, headers=self.headers).json()
        totals = int(r['paging']['totals'])
        title = r['data'][0]['question']['title']
        self.file_path = self.path.format(title)
        folder = os.path.exists(self.file_path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(self.file_path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        else:
            print('该问题内容已经有啦~')
            sys.exit()
        if totals % 20 == 0:
            max = int(totals / 20)
        else:
            max = int(totals / 20) + 1
        for m in range(max):
            offset = m * 20
            print('正在抓取第{}/{}页回答内容'.format(m + 1, max))
            self.get_urls(offset, m)
            time.sleep(3)
    @async  # 开启异步线程执行 调用一次开启一个线程
    def get_urls(self, offset, m):
        url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&offset={}&limit=20&sort_by=updated'.format(self.id, offset)
        dict = {
            'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
            'limit': 20,
            'offset': offset,
            'sort_by': 'updated'
        }
        r = requests.get(url, headers=self.headers, params=dict).json()
        datas = r['data']
        for data in datas:
            content = data['content']
            name = data['author']['name']
            if '知乎用户' == name:
                name = '{}{}'.format(name, self.zh_id)
                self.zh_id += 1
            if '「已注销」' == name:
                name = '{}{}'.format(name, self.zx_id)
                self.zx_id += 1
            if '匿名用户' == name:
                name = '{}{}'.format(name, self.nm_id)
                self.nm_id += 1
            if '[已重置]' == name:
                name = '{}{}'.format(name, self.cz_id)
                self.cz_id += 1
            timeStamp = int(data['updated_time'])
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
            img_names = []
            video_names = []
            img_urls = re.findall('<noscript><img src="(.*?)"', content, re.S)
            video_urls = re.findall('"z-ico-video"></span>(.*?)</span>', content, re.S)
            if img_urls:
                for i in range(len(img_urls)):
                    file_name = '{}({})_{}'.format(name, otherStyleTime, i+1)
                    img_names.append(file_name)
                if len(img_urls) == len(img_names):
                    data = [((img_url, img_name), None) for (img_url, img_name) in
                            zip(img_urls, img_names)]  # (index,i)也可以写成[index,i]
                    pool = threadpool.ThreadPool(15)
                    results = threadpool.makeRequests(self.save_img, data)
                    [pool.putRequest(req) for req in results]
                    pool.wait()
            if video_urls:
                for i in range(len(video_urls)):
                    file_name = '{}({})_video_{}'.format(name, otherStyleTime, i+1)
                    video_names.append(file_name)
                str_video_urls = str(video_urls)
                video_ids = re.findall(".*?/video/(.*?)'", str_video_urls, re.S)
                if len(video_ids) == len(video_names):
                    data = [((video_id, video_name), None) for (video_id, video_name) in zip(video_ids, video_names)]  # (index,i)也可以写成[index,i]
                    pool = threadpool.ThreadPool(15)
                    results = threadpool.makeRequests(self.save_video, data)
                    [pool.putRequest(req) for req in results]
                    pool.wait()
        print('第{}页回答内容获取完毕'.format(m + 1))
    def save_img(self, img_url, img_name):
        suffix = None
        if '.jpg' in img_url:
            suffix = '.jpg'
        elif '.gif' in img_url:
            suffix = '.gif'
        try:
            img = requests.get(img_url, headers=self.headers)
            if img.status_code == 200:
                with open(self.file_path + '/' + img_name + suffix, "wb") as f:
                    f.write(img.content)
                time.sleep(0.5)
            else:
                print('图片下载失败!', img.status_code)
        except:
            print(traceback.format_exc())
    def save_video(self, video_id, video_name):
        try:
            url = 'https://lens.zhihu.com/api/v4/videos/{}'.format(video_id)
            video_url = requests.get(url, headers=self.headers).json()['playlist']['LD']['play_url']
            video = requests.get(video_url, headers=self.headers)
            if video.status_code == 200:
                with open(self.file_path + '/' + video_name + '.mp4', "wb") as f:
                    f.write(video.content)
                time.sleep(0.5)
            else:
                print('视频下载失败!', video.status_code)
        except:
            print(traceback.format_exc())
if __name__ == '__main__':
    g = getZhiHuPic()
    g.get_offset()