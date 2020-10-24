import requests
import urllib3
import re
import json
import hashlib
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class instagram():
    def __init__(self,username):
        self.userName = username
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
        }
        self.path = "D:/instagram/{}/".format(self.userName)
        self.num = 1
        folder = os.path.exists(self.path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(self.path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    def get_index(self):
        url = 'https://www.instagram.com/{}/'.format(self.userName)
        # print(url)
        html = requests.get(url,headers=self.headers,verify=False).text
        sharedData = json.loads(re.findall('<script type="text/javascript">window._sharedData = (.*?);</script>', html, re.S)[0])
        user_id = re.findall('"profilePage_([0-9]+)"', html, re.S)[0]
        rhx_gis = re.findall('"rhx_gis":"([0-9a-z]+)"', html, re.S)[0]
        cursor = re.findall('"end_cursor":"(.*?)"', html, re.S)[0]
        count = re.findall('<meta property="og:description" content="(.*?)" />', html, re.S)[0]
        print(count)
        self.Posts =  re.findall('Following, (.*?) Posts - ', count, re.S)[0]
        query_cursor = cursor
        edges = sharedData['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        for edge in edges:
            shortcode = edge['node']['shortcode']
            p_url = 'https://www.instagram.com/p/{}/?__a=1'.format(shortcode)
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
                'X-Instagram-GIS': self.generate_x_instagram_gis(rhx_gis, cursor, user_id),
            }
            r = requests.get(p_url,headers=headers,verify=False)
            if r.status_code == 200:
                shortcode_media = r.json()['graphql']['shortcode_media']
                if shortcode_media['is_video']:
                    video_url = shortcode_media['video_url']
                    self.sava_video(video_url)
                else:
                    if 'edge_sidecar_to_children' in shortcode_media:
                        edges_list1 = shortcode_media['edge_sidecar_to_children']['edges']
                        for edges1 in edges_list1:
                            display_url = edges1['node']['display_url']
                            self.sava_img(display_url)
                    else:
                        display_url = shortcode_media['display_url']
                        self.sava_img(display_url)
                cursor = shortcode_media['edge_media_to_comment']['page_info']['end_cursor']
            else:
                print('index,出错了,{}'.format(r.status_code))
        self.query_hash(rhx_gis, query_cursor, user_id)
    def generate_x_instagram_gis(self, rhx_gis, cursor, user_id):
        params = {
            "id": user_id,
            "first": 12,
            "after": cursor,
        }
        json_params = json.dumps(params, separators=(',', ':'))
        values = "{}:{}".format(rhx_gis, json_params)
        md5 = hashlib.md5(values.encode('utf-8')).hexdigest()
        return md5
    def query_hash(self, rhx_gis, cursor, user_id):
        # print('2 query_cursor = {} ,{},{}'.format(cursor,rhx_gis,user_id))
        url = 'https://www.instagram.com/graphql/query/?'
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
            'X-Instagram-GIS': self.generate_x_instagram_gis(rhx_gis, cursor, user_id),
        }
        dict = {
            'query_hash': 'f2405b236d85e8296cf30347c9f08c2a',
            'variables': '{"id":"%s","first":12,"after":"%s"}'%(user_id,cursor)
        }
        r = requests.get(url,headers=headers,params=dict,verify=False)
        if r.status_code == 200:
            edges_list = r.json()['data']['user']['edge_owner_to_timeline_media']['edges']
            page_info = r.json()['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            for edges in edges_list:
                if edges['node']['is_video']:
                    video_url = edges['node']['video_url']
                    self.sava_video(video_url)
                else:
                    if 'edge_sidecar_to_children' in edges['node']:
                        edges_list1 = edges['node']['edge_sidecar_to_children']['edges']
                        for edges1 in edges_list1:
                            display_url = edges1['node']['display_url']
                            self.sava_img(display_url)
                    else:
                        display_url = edges['node']['display_url']
                        self.sava_img(display_url)
            if page_info == None:
                print('程序执行完毕~')
            else:
                self.query_hash(rhx_gis, page_info, user_id)
        else:
            print('出错了,{}'.format(r.status_code))
    def sava_img(self,display_url):
        img_name = hashlib.md5(display_url.encode('utf-8')).hexdigest()
        img = requests.get(display_url, headers=self.headers,verify=False)
        if img.status_code == 200:
            with open(self.path  + "{}.jpg".format(img_name), "wb") as f:
                f.write(img.content)
            print('已下载{}~,共{}个帖子'.format(self.num,self.Posts))
            self.num+=1
        else:
            print('图片下载出错了,状态码{}'.format(img.status_code))
    def sava_video(self,video_url):
        video_name = hashlib.md5(video_url.encode('utf-8')).hexdigest()
        video = requests.get(video_url, headers=self.headers,verify=False)
        if video.status_code == 200:
            with open(self.path  + "{}.mp4".format(video_name), "wb") as f:
                f.write(video.content)
            print('已下载{}~,共{}个帖子'.format(self.num,self.Posts))
            self.num+=1
        else:
            print('视频下载出错了,状态码{}'.format(video.status_code))
userNameList = [ 'chiaochiaotzeng', 'alephant_0427', 'pie__0124', 'kittie.118', '63official', 'baby19951111', 'ggshacylin', 'aejinlee_', 'rh_ab', 'berylovee', 'bad.asian.girl', 'ines.1017', 'vivihsu0317', 'pinksoulpuss', 'cawaiikanom', 'bcard.bcard', 'ohmybae', 'katotaka2.0official', '0_shufen', 'irenehuang8030', 'vivian19941008', 'tiffanylin9000', 'ago928', 'yui_xin_', 'showlo', 'gatitayan777',  'fei4809', 'jelly_jilli', 'morisakitomomi', 'yua_mikami', 'asukakiraran', 'chemiiiii', 'sugar_79']
for user in userNameList:
    ig = instagram(user)
    ig.get_index()