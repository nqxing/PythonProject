import requests
import re
import time
import pdfkit
class zhihu(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        self.id = '394248986'
        self.top_num = 1
        self.dic_str = {}
        self.new_content = ''
        self.hd_url = 'https://www.zhihu.com/question/{}/answer/{}'
        self.img_th_str = '<img src="{}">'
        self.video_th_str = '<p><img src="{}"></p><p><a href="{}">播放视频</a></p>'
    def sort_key(self, s):
        if s:
            try:
                c = re.findall('\d+$', s)[0]
            except:
                c = -1
            return int(c)
    def strsort(self, alist):
        alist.sort(key=self.sort_key, reverse=True)
        return alist
    def gets(self):
        url = 'https://www.zhihu.com/api/v4/questions/{}/answers'.format(self.id)
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            totals = int(r.json()['paging']['totals'])
            title = r.json()['data'][0]['question']['title']
            if totals % 20 == 0:
                self.max = int(totals / 20)
            else:
                self.max = int(totals / 20) + 1
            for m in range(self.max):
                offset = m * 20
                self.get_urls(offset, m + 1)
            print('处理完毕,正在对答案进行排序..')
            dic_list = self.strsort(list(self.dic_str.keys()))
            print('排序完成,正在拼接内容..')
            for d in dic_list:
                try:
                    self.new_content += self.dic_str[d]
                except:
                    print('Error')
            print('拼接成功,正在转换成PDF..')
            html = '<html><head><meta charset="UTF-8"><style>body{font-family:"微软雅黑";}a{text-decoration:none}.hd_url{ font-size:18px;text-indent:2em;}p{font-size:18px;}figure{margin: 0;padding: 0;border: 0;}</style></head><h1>%s个回答 - %s</h1>%s</html>' % (totals, title, self.new_content)
            config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
            # pdfkit.from_url('http://www.baidu.com', 'url_test.pdf',configuration=config) #通过url地址生成
            reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
            file_name = re.sub(reg, '', title)
            pdfkit.from_string(html, '{}.pdf'.format(file_name), configuration=config)
    def get_urls(self, offset, m):
        print('共{}页,正在处理第{}页内容..'.format(self.max, m))
        try:
            url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&offset={}&limit=20&sort_by=updated'.format(
                self.id, offset)
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
                timeStamp = int(data['updated_time'])
                timeArray = time.localtime(timeStamp)
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                voteup_count = int(data['voteup_count'])
                headline = data['author']['headline']
                hd_id = int(data['id'])
                img_urls = re.findall('<noscript><img src="(.*?)"', content, re.S)
                # quc_strs = re.findall('<figure data-size=".*?">(.*?)</figure>', content, re.S)
                quc_strs = re.findall('<figure.*?>(.*?)</figure>', content, re.S)
                tit_str = '<h1>{}({})</h1><div><div class="hd_url">更新时间：{}&nbsp;&nbsp;&nbsp;&nbsp;签名：{}</div>'.format(name, voteup_count, otherStyleTime, headline)
                video_urls = re.findall('"z-ico-video"></span>(.*?)</span>', content, re.S)
                video_quc_strs = re.findall('<a class="video-box" href="(.*?)</a>', content, re.S)
                if img_urls and quc_strs:
                    if len(img_urls) == len(quc_strs):
                        for i in range(len(quc_strs)):
                            if quc_strs[i] in content:
                                content = content.replace(quc_strs[i], self.img_th_str.format(img_urls[i]))
                if video_urls and video_quc_strs:
                    if len(video_urls) == len(video_quc_strs):
                        for i in range(len(video_quc_strs)):
                            if video_quc_strs[i] in content:
                                video_img_url = re.findall('src="(.*?)"', video_quc_strs[i], re.S)
                                content = content.replace('<a class="video-box" href="{}</a>'.format(video_quc_strs[i]), self.video_th_str.format(video_img_url[0], video_urls[i]))

                content = tit_str + content + '</div><div class="hd_url"><a href="{}">>>去知乎查看这个回答</a></div>'.format(self.hd_url.format(self.id, hd_id))
                # self.new_content += content
                self.dic_str['{}_{}'.format(self.top_num, voteup_count)] = content
                self.top_num += 1
        except Exception as e:
            # pass
            print(e)
def main():
    # 初始化对象
    L = zhihu()
    # 进行布局
    L.gets()
if __name__ == '__main__':
    main()