# 获取掌上英雄联盟的所有壁纸
import requests
import pymysql

HOST = '122.51.67.37'
USER = 'root'
# PWD = 'MUGVHmugvtwja116ye38b1jhb'
PWD = 'mm123456'

mysql_conn = pymysql.connect(host=HOST, user=USER, password=PWD, port=3306, db="public")
mysql_cursor = mysql_conn.cursor()  # 获取游标

for i in range(100):
    r = requests.get("http://qt.qq.com/php_cgi/lol_goods/varcache_wallpaper_list.php?type=new&page={}&num=20&plat=ios&version=9940".format(i)).json()
    print(i)
    if "wallpapers" in r:
        for w in r['wallpapers']:
            skin_name = w["name"]
            skin_url = w["url"]
            hero_name = "掌盟#{}".format(w["id"])
            sql = "INSERT INTO pub_lol_wall (skin_name, skin_url, hero_name,hero_id) VALUES ('{}', '{}', '{}',{})".format(
                skin_name, skin_url, hero_name,1000)
            mysql_cursor.execute(sql)
            mysql_conn.commit()
    else:
        break
