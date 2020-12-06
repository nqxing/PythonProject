import requests
import re
import pymysql
import datetime
# 禁用安全请求警告 关闭SSL验证时用
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# HOST = 'localhost'
HOST = '116.62.126.139'
USER = 'root'
# PWD = 'MUGVHmugvtwja116ye38b1jhb'
PWD = 'mm123456'
mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db='pub_zqwz')
mysql_cursor = mysql_conn.cursor()  # 获取游标


cookie = """
pgv_pvid=1364724232; pgv_pvi=458578944; RK=9DRo5K2gNs; ptcz=604e3a089b8f6a2ccace670331f07a16bbca31a3407fbc64731d4384bf5933a4; tvfe_boss_uuid=b37637d68b9600b0; LW_uid=j1E5J7R7t8v8J7m1W8d3u7j0g8; eas_sid=p1H5x7z7u83867D1w8m3D793R0; LW_sid=S1V5C7r7v8q837L2X0Z7y3O329; ptui_loginuin=781583148; cookie_passkey=1; uin=Nzc0MjkzNTIy; key=bc1dc83c74ff7841038b82153c35c4fad936e9f67b26994be698fdfd772a5938bc2deba25ac24330d10d57970af2eb76d38a8db649437c2851654fbfba09dccc0915d1232c9f8ab67460756b9634f0337493b95bec40180635abd567cb3deea91a3191dd20f1f97e79c58d3a8f1413611a500331300d14f11900648ad3f51d8e; pass_ticket=4rlKZPiBaF6AOE3vQ9jat%2FO04DAR6HTXX3En8HWzVgobLEaUuydiHXZSEl1XTTvB; __guid=56367293.1877497896910427000.1607165866046.7485; monitor_count=2
"""

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
	"Cookie": "pgv_pvid=1364724232; pgv_pvi=458578944; RK=9DRo5K2gNs; ptcz=604e3a089b8f6a2ccace670331f07a16bbca31a3407fbc64731d4384bf5933a4; tvfe_boss_uuid=b37637d68b9600b0; LW_uid=j1E5J7R7t8v8J7m1W8d3u7j0g8; eas_sid=p1H5x7z7u83867D1w8m3D793R0; LW_sid=S1V5C7r7v8q837L2X0Z7y3O329; ptui_loginuin=781583148; cookie_passkey=1; uin=Nzc0MjkzNTIy; key=bc1dc83c74ff7841038b82153c35c4fad936e9f67b26994be698fdfd772a5938bc2deba25ac24330d10d57970af2eb76d38a8db649437c2851654fbfba09dccc0915d1232c9f8ab67460756b9634f0337493b95bec40180635abd567cb3deea91a3191dd20f1f97e79c58d3a8f1413611a500331300d14f11900648ad3f51d8e; pass_ticket=4rlKZPiBaF6AOE3vQ9jat%2FO04DAR6HTXX3En8HWzVgobLEaUuydiHXZSEl1XTTvB; __guid=56367293.1877497896910427000.1607165866046.7485; monitor_count=2"
}


mysql_cursor.execute('select * from pub_wz_hero_name')
values = mysql_cursor.fetchall()
for v in values:
	# print(v)
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
	# print(herotpl)
	if herotpl['errmsg'] == 'ok':
		html_tpl = herotpl['hero_tpl']['html_tpl']
		texts = re.findall('<div class="hero__info-content">(.*?)</div>', html_tpl, re.S)
		titles = ['技能升级', '铭文搭配', '打法攻略', '团战攻略']
		if len(texts) == len(titles):
			mysql_cursor.execute('select cx_value from pub_wz_win_rate where hero_id = {}'.format(game_hero_id))
			value = mysql_cursor.fetchall()[0]
			csHeroInfo = value[0].split('|')[0]
			for i,t in enumerate(texts):
				ss = '||【{}】|{}'.format(titles[i], t.strip())
				csHeroInfo += ss
			# print(csHeroInfo)

	herogoddata = requests.post('https://game.weixin.qq.com/cgi-bin/gamewap/gameherogoddata?uin=&key=&pass_ticket=&QB&', headers=headers, json=jsondata2, verify=False).json()
	# print(herogoddata)
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
	print('-------------------------------------------')
	print(hero_cxNames)
	print(god_equips)
	print(csHeroInfo)
	for h in hero_cxNames:
		hs1 = '{}出装'.format(h)
		mysql_cursor.execute('''select * from pub_wz_equip where cx_name = "{}"'''.format(hs1))
		values = mysql_cursor.fetchall()
		if values:
			sql = '''UPDATE pub_wz_equip SET cx_value1 = "{}" WHERE cx_name = "{}" '''.format(god_equips, hs1)
			mysql_cursor.execute(sql)
			mysql_conn.commit()
		hs2 = '{}攻略'.format(h)
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
