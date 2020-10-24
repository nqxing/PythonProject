import requests
import re
import os
import time
from threading import Thread

def async(f):
    def wrapper(*args, **kwargs):
        # print(args)
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

class getZhiHuPic:
    def __init__(self):
        #
        self.id = 328798732
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        self.name_id = 1
        # self.hd_url = 'https://{}/80/v2-{}_hd.jpg'
        self.zz = re.compile('<noscript><img src="(.*?)"', re.S)
        # self.zz1 = re.compile('.*?//(.*?)/v2-(.*?)_b', re.S)
        self.img_path = "D:/知乎答案图片/%s" % self.id
        folder = os.path.exists(self.img_path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(self.img_path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    def structureUrl(self):
        url = 'https://www.zhihu.com/api/v4/questions/{}/answers'.format(self.id)
        r = requests.get(url, headers=self.headers).json()
        totals = int(r['paging']['totals'])
        if totals % 20 == 0:
            max = int(totals / 20)
        else:
            max = int(totals / 20) + 1
        for m in range(max):
            offset = m * 20
            print('正在抓取第{}/{}页回答图片~~'.format(m + 1,max))
            self.savePic(offset, m)
            time.sleep(5)
    @async  # 开启异步线程执行 调用一次开启一个线程
    def savePic(self, offset, m):
        url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&offset={}&limit=20&sort_by=updated'.format(self.id, offset)
        dict = {
            'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_labeled;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics',
            'limit': 20,
            'offset': offset,
            'sort_by': 'updated'
        }
        r = requests.get(url, headers=self.headers, params=dict).json()
        # print(r)
        dataList = r['data']
        for data in dataList:
            content = data['content']
            name = data['author']['name']
            if '知乎用户' == name:
                name = '{}{}'.format(name, self.name_id)
                self.name_id += 1
            timeStamp = int(data['updated_time'])
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y-%m-%d", timeArray)

            img_urls = re.findall(self.zz, content)
            # print(b_url)
            if img_urls:
                for i in range(len(img_urls)):
                    file_name = '{}({})_{}'.format(name, otherStyleTime, i+1)
                    # r = re.findall(self.zz1, b)
                    # if r and len(r[0])==2:
                        # hdurl = self.hd_url.format(r[0][0], r[0][1])
                    img = requests.get(img_urls[i], headers=self.headers)
                    if img.status_code == 200:
                        with open(self.img_path + '/' + file_name + ".jpg", "wb") as f:
                            f.write(img.content)
                        time.sleep(0.5)
                    else:
                        print('出现错误~')
                        print(r)
        print('第{}页回答图片获取完毕~~'.format(m + 1))
if __name__ == '__main__':
    g = getZhiHuPic()
    g.structureUrl()