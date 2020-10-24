import requests
import re
import urllib3
import json
import hashlib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class insUserName():
    def __init__(self):
        self.id = '10648256385'
        self.usernamelist = []
    def get_rhx_gis(self):
        login_url = 'https://www.instagram.com/accounts/login/'
        html = requests.get(login_url,verify=False).text
        rhx_gis = re.findall('"rhx_gis":"([0-9a-z]+)"', html, re.S)[0]
        variables = '{"id":"%s","include_reel":true,"fetch_mutual":false,"first":24}'%self.id
        XInstagramGIS = self.generate_x_instagram_gis(rhx_gis)
        self.get_userName(rhx_gis,variables,XInstagramGIS)
    def get_userName(self,rhx_gis,variables,XInstagramGIS):
        url = 'https://www.instagram.com/graphql/query/?'
        dict = {
            'query_hash': 'c56ee0ae1f89cdbd1c89e2bc6b8f3d18',
            'variables': variables
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
            # 'X-Instagram-GIS': '13dae715008727da00d3a8aff2b9d1c2',
            'X-Instagram-GIS': XInstagramGIS,
            'Cookie': 'sessionid=10648256385%3AQaLtZFshGD5goL%3A6;'
        }
        r = requests.get(url,params=dict,headers=headers,verify=False).json()
        userNameList = r['data']['user']['edge_follow']['edges']
        end_cursor = r['data']['user']['edge_follow']['page_info']['end_cursor']
        for userName in userNameList:
            username = userName['node']['username']
            self.usernamelist.append(username)
        if end_cursor == None:
            print('共获取{}位用户~'.format(len(self.usernamelist)))
            with open("userName.txt", "w", encoding='utf-8') as f:
                f.write(str(self.usernamelist))
            print('程序执行完毕~')
        else:
            variables = '{"id":"%s","include_reel":true,"fetch_mutual":false,"first":12,"after":"%s"}'%(self.id,end_cursor)
            XInstagramGIS = self.generate_x_instagram_gis1(rhx_gis, end_cursor)
            self.get_userName(rhx_gis,variables,XInstagramGIS)
    def generate_x_instagram_gis(self,rhx_gis):
        par = {"id":"{}".format(self.id),"include_reel":True,"fetch_mutual":False,"first":24}
        json_params = json.dumps(par, separators=(',', ':'))
        values = "{}:{}".format(rhx_gis, json_params)
        return hashlib.md5(values.encode('utf-8')).hexdigest()
    def generate_x_instagram_gis1(self,rhx_gis, cursor):
        par = {"id":"{}".format(self.id),"include_reel":True,"fetch_mutual":False,"first":12,"after": cursor}
        json_params = json.dumps(par, separators=(',', ':'))
        values = "{}:{}".format(rhx_gis, json_params)
        return hashlib.md5(values.encode('utf-8')).hexdigest()
    def login(self):
        post_url = 'https://www.instagram.com/accounts/login/ajax/'
        get_url = 'https://www.instagram.com/accounts/login/'
        headers = {
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 'X-Instagram-AJAX': '3ecfbff24fce',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
        }
        dict = {
            'username': 'iwx7080',
            'password': 'mm231798',
            'queryParams': {},
            'optIntoOneTap': False
        }
        r = requests.get(get_url, headers=headers, verify=False)
        XInstagramAJAX = re.findall('"rollout_hash":"([0-9a-z]+)"', r.text, re.S)[0]
        print(XInstagramAJAX)
        headers['X-Instagram-AJAX'] = XInstagramAJAX
        headers['Referer'] = get_url
        headers['X-CSRFToken'] = r.cookies['csrftoken']
        r1 = requests.post(post_url,headers=headers,data=dict,verify=False)
        if r1.status_code == 400:
            checkpoint_url = 'https://www.instagram.com{}'.format(r1.json()['checkpoint_url'])
            print(checkpoint_url)
            # r12 = requests.get(checkpoint_url, headers=headers, verify=False)
            # print(r12.text)
            # print(r12.cookies)
            # print('---------------------------------------------------')
            headers['Referer'] = checkpoint_url
            r2 = requests.post(checkpoint_url,headers=headers,data={'choice': 1},verify=False)
            print(r2.text)
            print(r2.status_code)
            d_dict = {
                'security_code':int(input('请输入验证码：'))
            }
            r3 = requests.post(checkpoint_url, headers=headers, data=d_dict, verify=False)
            print(r3.status_code)
            print(r3.text)
            print(r3.cookies)
        # print(headers)
        # print(r1.text)
        # print(r1.status_code)
        # print(r1.cookies)
o = insUserName()
o.login()