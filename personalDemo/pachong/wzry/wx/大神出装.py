import requests
import re
import pymysql
import datetime
# 禁用安全请求警告 关闭SSL验证时用
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# HOST = 'localhost'
HOST = '122.51.67.37'
USER = 'root'
# PWD = 'MUGVHmugvtwja116ye38b1jhb'
PWD = 'mm123456'
mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='public')
mysql_cursor = mysql_conn.cursor()  # 获取游标
headers = {
	"Host": "game.weixin.qq.com",
	"Connection": "keep-alive",
	"Content-Length": "84",
	"Pragma": "no-cache",
	"Cache-Control": "no-cache",
	"Origin": "https://game.weixin.qq.com",
	"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080",
	"Content-Type": "application/json; charset=UTF-8",
	"Accept": "*/*",
	"Sec-Fetch-Site": "same-origin",
	"Sec-Fetch-Mode": "cors",
	"Referer": "https://game.weixin.qq.com/cgi-bin/h5/static/zone/hero.html?keyword=%E4%B8%8A%E5%AE%98%E5%A9%89%E5%84%BF&ssid=2103&appid=wx95a3a4d7c627e07d&game_hero_id=513&hero_id=153",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "zh-CN,zh;q=0.9",
	"Cookie": "uin=Nzc0MjkzNTIy; key=fc8f003c4b06af77d4ead99ebb3372759880c9d08e5fe7e79f4278bb313319a301ff2743207caf58e59b351434ece422eb0135fc1d617db67413d2829cf847c528d81a101fecfa7468d26662efbc5b0d; pass_ticket=yW8O1w685iGnWQuqNQnVNLdxKqB721v5mQDZqTH8n4XuYdZ6xJDL4xGb7KFkbHNw"
}


mysql_cursor.execute('select * from pub_wz_hero_name')
values = mysql_cursor.fetchall()
for v in values:
	print(v)
	csHeroInfo = ''
	god_equips = ''
	hero_name_bm = v[3]
	hero_cxNames = [v[2]]
	if hero_name_bm != None:
		if '|' in hero_name_bm:
			hero_cxNames += hero_name_bm.split('|')
		else:
			hero_cxNames.append(hero_name_bm)
	game_hero_id = v[1]
	jsondata1 = {"appid":"wx95a3a4d7c627e07d", "game_hero_id": game_hero_id}
	jsondata2 = {
		"appid": "wx95a3a4d7c627e07d",
		"platform": 1,
		"game_hero_id": game_hero_id,
		"offset": 0,
		"limit": 10
	}
	herotpl = requests.post('https://game.weixin.qq.com/cgi-bin/gamewap/gameherotpl', headers=headers, json=jsondata1, verify=False).json()
	if herotpl['errmsg'] == 'ok':
		html_tpl = herotpl['hero_tpl']['html_tpl']
		texts = re.findall('<div class="hero__info-content">(.*?)</div>', html_tpl, re.S)
		titles = ['技能升级技巧', '铭文搭配技巧', '使用技巧', '团战技巧']
		if len(texts) == len(titles):
			mysql_cursor.execute('select cx_value from pub_wz_win_rate where hero_id = {}'.format(game_hero_id))
			value = mysql_cursor.fetchall()[0]
			csHeroInfo = value[0].split('|')[0]
			for i,t in enumerate(texts):
				ss = '||【{}】|{}'.format(titles[i], t.strip())
				csHeroInfo += ss
			# print(csHeroInfo)

	herogoddata = requests.post('https://game.weixin.qq.com/cgi-bin/gamewap/gameherogoddata?uin=&key=&pass_ticket=&QB&', headers=headers, json=jsondata2, verify=False).json()
	if herogoddata['errmsg'] == 'ok':
		god_equip_list = herogoddata['great_god_equip']['god_equip_list']
		for i,g in enumerate(god_equip_list):
			equip_list = g['equip_list']
			equips = '||【大神出装{}】|'.format(i+1)
			game_count = g['game_count']
			win_count = g['win_count']
			for k,e in enumerate(equip_list):
				es = '{} '.format(e['title'])
				if k == 2:
					es = es.strip() + '|'
				equips += es
			equips = equips.strip()
			wins = '|胜率{}% 胜场数{}'.format('%.2f' % float(win_count/game_count*100), win_count)
			equips += wins
			god_equips += equips
			if i == 2:
				break
	for h in hero_cxNames:
		hs1 = '{}出装'.format(h)
		mysql_cursor.execute('''select * from pub_wz_equip where cx_name = "{}"'''.format(hs1))
		values = mysql_cursor.fetchall()
		if values:
			sql = '''UPDATE pub_wz_equip SET cx_value1 = "{}" WHERE cx_name = "{}" '''.format(god_equips, hs1)
			mysql_cursor.execute(sql)
			mysql_conn.commit()
		hs2 = '{}技巧'.format(h)
		mysql_cursor.execute('''select * from pub_wz_skills where cx_name = "{}"'''.format(hs2))
		values = mysql_cursor.fetchall()
		if values:
			sql = '''UPDATE pub_wz_skills SET cx_value = "{}",update_time="{}" WHERE cx_name = "{}" '''.format(csHeroInfo,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), hs2)
			mysql_cursor.execute(sql)
			mysql_conn.commit()
		else:
			sql = "INSERT INTO pub_wz_skills (cx_name, cx_value, hero_name, hero_id, update_time) VALUES ('{}', '{}', '{}', {}, '{}')".format(hs2, csHeroInfo, v[2], game_hero_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
			mysql_cursor.execute(sql)
			mysql_conn.commit()
